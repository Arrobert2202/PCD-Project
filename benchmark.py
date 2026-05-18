#!/usr/bin/env python3
"""
OCR Benchmark Script

Downloads a Kaggle OCR dataset, runs it through the backend, and reports
WER / CER statistics per engine.

Setup:
    pip install kaggle requests
    Place your Kaggle credentials in ~/.kaggle/kaggle.json
    (or set KAGGLE_USERNAME and KAGGLE_KEY environment variables)

Usage:
    python benchmark.py
    python benchmark.py --engines easyocr tesseract paddleocr
    python benchmark.py --dataset nageshsingh/the-street-view-text-dataset --limit 200
    python benchmark.py --output results.json
"""

import argparse
import base64
import csv
import io
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from statistics import mean
from typing import Optional

import kaggle
import requests
from PIL import Image

# ── defaults ────────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000"
DEFAULT_DATASET = "ssarkar445/handwriting-recognitionocr"
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
BATCH_SIZE = 16


# ── dataset download ─────────────────────────────────────────────────────────

def download_dataset(dataset: str, dest: Path) -> Path:
    extract_dir = dest / "extracted"
    if extract_dir.exists():
        print(f"Using cached dataset at {extract_dir}")
        return extract_dir

    extract_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {dataset} ...")

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=str(extract_dir), unzip=True)

    return extract_dir


# ── ground truth detection ───────────────────────────────────────────────────

def _iter_images(root: Path):
    for p in root.rglob("*"):
        if p.suffix.lower() in IMAGE_EXTS:
            yield p


def _parse_svt_xml(xml_file: Path, crop_dir: Path) -> list[tuple[Path, str]]:
    """
    Parse an SVT-style XML file (train.xml / test.xml).
    Crops each tagged word region from its source image and saves it to
    crop_dir, returning (crop_path, word_text) pairs.

    Expected XML structure:
        <tagset>
          <image>
            <imageName>img/00_00.jpg</imageName>
            <taggedRectangles>
              <taggedRectangle x="10" y="20" width="80" height="30">
                <tag>WORD</tag>
              </taggedRectangle>
            </taggedRectangles>
          </image>
        </tagset>
    """
    crop_dir.mkdir(parents=True, exist_ok=True)
    root_dir = xml_file.parent
    pairs: list[tuple[Path, str]] = []

    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        return pairs

    for image_elem in tree.getroot():
        name_elem = image_elem.find("imageName")
        if name_elem is None or not name_elem.text:
            continue

        img_path = root_dir / name_elem.text.strip()
        if not img_path.exists():
            continue

        try:
            img = Image.open(img_path).convert("RGB")
        except Exception:
            continue

        for rect in image_elem.findall(".//taggedRectangle"):
            tag_elem = rect.find("tag")
            if tag_elem is None or not (tag_elem.text or "").strip():
                continue
            word = tag_elem.text.strip()

            try:
                x = int(rect.attrib["x"])
                y = int(rect.attrib["y"])
                w = int(rect.attrib["width"])
                h = int(rect.attrib["height"])
            except (KeyError, ValueError):
                continue

            if w <= 0 or h <= 0:
                continue

            crop = img.crop((x, y, x + w, y + h))
            crop_path = crop_dir / f"{img_path.stem}_{x}_{y}_{w}_{h}.jpg"
            if not crop_path.exists():
                clean = Image.new("RGB", crop.size)
                clean.paste(crop)
                clean.save(crop_path, format="JPEG", quality=95)
            pairs.append((crop_path, word))

    return pairs


def load_ground_truth(root: Path, limit: Optional[int], cache_dir: Path) -> list[tuple[Path, str]]:
    """
    Try five layouts in order:
      0. SVT XML        (train.xml / test.xml with <taggedRectangle> elements)
      1. CSV manifest   (columns: filename/image + text/label/transcript)
      2. JSON manifest  (list of {filename, text} objects)
      3. Side-car .txt  (image.jpg → image.txt)
      4. Folder name    (word-level datasets where parent dir = ground truth)
    """
    pairs: list[tuple[Path, str]] = []

    # 0 – SVT XML (prefer test.xml, fall back to train.xml)
    for xml_name in ("test.xml", "train.xml"):
        for xml_file in sorted(root.rglob(xml_name)):
            crop_dir = cache_dir / "svt_crops"
            parsed = _parse_svt_xml(xml_file, crop_dir)
            if parsed:
                pairs.extend(parsed)
                print(f"Ground truth: SVT XML ({xml_file.relative_to(root)})  —  {len(parsed)} word crops")
                break
        if pairs:
            break

    # 1 – CSV manifest
    if not pairs:
        for csv_file in sorted(root.rglob("*.csv")):
            try:
                with open(csv_file, newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    fields = [c.lower() for c in (reader.fieldnames or [])]
                    img_col = _pick(reader.fieldnames, fields, ("filename", "image", "file", "img"))
                    txt_col = _pick(reader.fieldnames, fields, ("text", "label", "transcript", "word", "annotation"))
                    if not img_col or not txt_col:
                        continue
                    for row in reader:
                        p = root / row[img_col]
                        if p.exists() and p.suffix.lower() in IMAGE_EXTS:
                            pairs.append((p, row[txt_col].strip()))
            except Exception:
                continue
            if pairs:
                print(f"Ground truth: CSV manifest ({csv_file.relative_to(root)})")
                break

    # 2 – JSON manifest
    if not pairs:
        for json_file in sorted(root.rglob("*.json")):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                if not isinstance(data, list):
                    continue
                for item in data:
                    img = item.get("filename") or item.get("image") or item.get("file")
                    txt = item.get("text") or item.get("label") or item.get("transcript")
                    if img and txt:
                        p = root / str(img)
                        if p.exists():
                            pairs.append((p, str(txt).strip()))
            except Exception:
                continue
            if pairs:
                print(f"Ground truth: JSON manifest ({json_file.relative_to(root)})")
                break

    # 3 – side-car .txt
    if not pairs:
        for p in _iter_images(root):
            txt_path = p.with_suffix(".txt")
            if txt_path.exists():
                pairs.append((p, txt_path.read_text(encoding="utf-8").strip()))
        if pairs:
            print("Ground truth: side-car .txt files")

    # 4 – folder name as label
    if not pairs:
        for p in _iter_images(root):
            label = p.parent.name.replace("_", " ").strip()
            if label:
                pairs.append((p, label))
        if pairs:
            print("Ground truth: folder name as label")

    if not pairs:
        print("Error: could not detect ground truth annotations in the dataset.")
        print("Supported layouts: SVT XML, CSV/JSON manifest, side-car .txt, folder-name label.")
        sys.exit(1)

    print(f"Total pairs: {len(pairs)}")
    if limit:
        pairs = pairs[:limit]
        print(f"Limited to {limit} images.")
    return pairs


def _pick(originals, lowered, candidates):
    for c in candidates:
        if c in lowered:
            return originals[lowered.index(c)]
    return None


# ── evaluation ───────────────────────────────────────────────────────────────

def encode_image(path: Path) -> Optional[str]:
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return None


def run_evaluation(pairs: list, engine: str, lang: str, url: str) -> list[dict]:
    results = []
    total = len(pairs)

    for start in range(0, total, BATCH_SIZE):
        batch = pairs[start : start + BATCH_SIZE]
        items = []
        for img_path, expected in batch:
            b64 = encode_image(img_path)
            if b64 is None:
                continue
            items.append({"image": b64, "expected_text": expected})

        if not items:
            continue

        try:
            resp = requests.post(
                f"{url}/evaluate/batch",
                json={"items": items, "engine": engine, "lang": lang},
                timeout=120,
            )
            resp.raise_for_status()
            results.extend(resp.json()["results"])
        except requests.RequestException as e:
            print(f"\n  Batch {start // BATCH_SIZE + 1} error: {e}")

        done = min(start + BATCH_SIZE, total)
        print(f"  {done}/{total} processed ...", end="\r", flush=True)

    print()
    return results


# ── statistics ───────────────────────────────────────────────────────────────

def compute_stats(engine: str, results: list[dict]) -> dict:
    valid   = [r for r in results if r.get("wer") is not None]
    errors  = sum(1 for r in results if r.get("status") == "error")
    no_text = sum(1 for r in results if r.get("status") == "no_text_detected")

    if not valid:
        return {}

    wers   = [r["wer"] for r in valid]
    cers   = [r["cer"] for r in valid if r.get("cer") is not None]
    perfect = sum(1 for w in wers if w == 0.0)

    return {
        "engine":          engine,
        "samples":         len(results),
        "evaluated":       len(valid),
        "errors":          errors,
        "no_text":         no_text,
        "mean_wer":        round(mean(wers), 4),
        "mean_cer":        round(mean(cers), 4) if cers else None,
        "perfect_matches": perfect,
    }


def print_stats(stats: dict):
    if not stats:
        print("  No valid results.")
        return

    evald   = stats["evaluated"]
    perfect = stats["perfect_matches"]
    cer_str = f"{stats['mean_cer']*100:.2f}%" if stats["mean_cer"] is not None else "n/a"

    print(f"\n  Engine          : {stats['engine']}")
    print(f"  Samples         : {stats['samples']}  |  Evaluated: {evald}  |  Errors: {stats['errors']}  |  No text: {stats['no_text']}")
    print(f"  Mean WER        : {stats['mean_wer']*100:.2f}%")
    print(f"  Mean CER        : {cer_str}")
    print(f"  Perfect matches : {perfect}/{evald}  ({perfect/evald*100:.1f}%)")


def print_comparison_table(all_stats: list[dict]):
    if len(all_stats) < 2:
        return
    ranked = sorted(all_stats, key=lambda s: s.get("mean_wer", 1.0))
    print("\n" + "═" * 58)
    print(f"  {'Engine':<14} {'WER':>8} {'CER':>8} {'Perfect':>10} {'Samples':>8}")
    print("─" * 58)
    for s in ranked:
        cer  = f"{s['mean_cer']*100:.2f}%" if s.get("mean_cer") is not None else "   n/a"
        perf = f"{s['perfect_matches']}/{s['evaluated']}"
        print(f"  {s['engine']:<14} {s['mean_wer']*100:>7.2f}% {cer:>8} {perf:>10} {s['samples']:>8}")
    print("═" * 58)
    print(f"  Best: {ranked[0]['engine']}")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Benchmark backend OCR engines against a Kaggle dataset."
    )
    parser.add_argument(
        "--dataset", default=DEFAULT_DATASET,
        help="Kaggle dataset identifier (owner/name)",
    )
    parser.add_argument(
        "--engines", nargs="+", default=["easyocr"],
        choices=["easyocr", "tesseract", "paddleocr"],
        metavar="ENGINE",
        help="One or more engines to evaluate (default: easyocr)",
    )
    parser.add_argument(
        "--lang", default="auto",
        help="Language code passed to the backend, or 'auto' (default: auto)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max number of images to evaluate (default: all)",
    )
    parser.add_argument(
        "--url", default=BACKEND_URL,
        help=f"Backend base URL (default: {BACKEND_URL})",
    )
    parser.add_argument(
        "--output", default=None,
        help="Save full per-image results to a JSON file",
    )
    parser.add_argument(
        "--data-dir", default=".benchmark_cache",
        help="Local directory for cached downloads (default: .benchmark_cache)",
    )
    args = parser.parse_args()

    try:
        requests.get(f"{args.url}/health", timeout=5).raise_for_status()
        print(f"Backend reachable at {args.url}")
    except Exception:
        print(f"Error: backend not reachable at {args.url}  (is it running?)")
        sys.exit(1)

    data_dir    = Path(args.data_dir)
    extract_dir = download_dataset(args.dataset, data_dir)
    pairs       = load_ground_truth(extract_dir, args.limit, data_dir)

    all_stats: list[dict] = []
    full_output: dict = {}

    for engine in args.engines:
        print(f"\n── Evaluating [{engine}] ──────────────────────────")
        results = run_evaluation(pairs, engine, args.lang, args.url)
        stats   = compute_stats(engine, results)
        print_stats(stats)
        if stats:
            all_stats.append(stats)
        full_output[engine] = {"stats": stats, "results": results}

    print_comparison_table(all_stats)

    if args.output:
        Path(args.output).write_text(json.dumps(full_output, indent=2), encoding="utf-8")
        print(f"\nFull results saved to {args.output}")


if __name__ == "__main__":
    main()
