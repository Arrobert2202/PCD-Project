#!/usr/bin/env python3
"""
Evaluate OCR backend on prepared dataset and export results to CSV.
Usage: python benchmark_eval.py [--photos test_photos] [--gt test_photos/ground_truth.json]
"""

import argparse
import ast
import base64
import csv
import json
import sys
import time
from pathlib import Path
from statistics import mean

try:
    import requests
except ImportError:
    print("Missing dependency: requests")
    print("Run: pip install requests")
    sys.exit(1)

BACKEND_URL = "http://localhost:8000"
IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
REQUEST_TIMEOUT = 120

SCENARIOS = [
    {"name": "Baseline",  "engine": "tesseract", "fuzzy": False, "lang": "en"},
    {"name": "Optimized", "engine": "easyocr",   "fuzzy": True,  "lang": "en"},
    {"name": "Optimized", "engine": "paddleocr",   "fuzzy": False,  "lang": "auto"}
]

CSV_COLUMNS = ["image", "scenario", "engine", "fuzzy", "wer", "cer", "latency_s", "status", "detected_language"]


def _iter_top_level_literals(s):
    """Yield substrings of s corresponding to top-level Python literals ({ } or [ ])."""
    openers = {'{': '}', '[': ']', '(': ')'}
    closers = set(openers.values())
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i].isspace():
            i += 1
        if i >= n:
            break
        if s[i] not in openers:
            i += 1
            continue
        depth, in_str, str_char, j = 0, False, None, i
        while j < n:
            ch = s[j]
            if in_str:
                if ch == '\\':
                    j += 2
                    continue
                if ch == str_char:
                    in_str = False
            elif ch in ('"', "'"):
                in_str, str_char = True, ch
            elif ch in openers:
                depth += 1
            elif ch in closers:
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        yield s[i:j]
        i = j


def _build_text_from_sroie_annotations(annotation_list):
    """Reconstruct reading-order text from a SROIE word-annotation list."""
    rows = {}
    for entry in annotation_list:
        for word in entry.get('words', []):
            text = word.get('text', '').strip()
            if not text:
                continue
            row_id = word.get('row_id', 0)
            quad = word.get('quad', {})
            x1 = quad.get('x1', 0)
            y1 = quad.get('y1', 0)
            if row_id not in rows:
                rows[row_id] = {'y1': y1, 'words': []}
            rows[row_id]['words'].append((x1, text))

    lines = []
    for row in sorted(rows.values(), key=lambda r: r['y1']):
        line_words = sorted(row['words'], key=lambda w: w[0])
        lines.append(' '.join(w[1] for w in line_words))
    return '\n'.join(lines)


def parse_sroie_value(raw_value):
    """
    Each ground_truth.json value is a concatenation of Python literals.
    The one that is a list of dicts with 'words'/'category' keys holds the
    word-level annotations. Extract and reconstruct the receipt text from it.
    Returns the raw string unchanged if no annotation list is found.
    """
    for obj_str in _iter_top_level_literals(raw_value):
        if not obj_str.startswith('['):
            continue
        try:
            obj = ast.literal_eval(obj_str)
        except Exception:
            continue
        if isinstance(obj, list) and obj and isinstance(obj[0], dict) and 'words' in obj[0]:
            return _build_text_from_sroie_annotations(obj)
    return raw_value


def encode(path):
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return None


def call_evaluate(url, image_b64, expected, scenario):
    payload = {
        "image": image_b64,
        "expected_text": expected,
        "engine": scenario["engine"],
        "fuzzy": scenario["fuzzy"],
        "lang": scenario["lang"],
    }
    t0 = time.perf_counter()
    try:
        r = requests.post(f"{url}/evaluate", json=payload, timeout=REQUEST_TIMEOUT)
        latency = round(time.perf_counter() - t0, 4)
        r.raise_for_status()
        return r.json(), latency
    except requests.exceptions.Timeout:
        return {"status": "timeout", "wer": None, "cer": None, "language": None}, round(time.perf_counter() - t0, 4)
    except requests.exceptions.RequestException as e:
        return {"status": f"error: {e}", "wer": None, "cer": None, "language": None}, round(time.perf_counter() - t0, 4)


def check_backend(url):
    print(f"Checking backend at {url}...", end=" ", flush=True)
    try:
        requests.get(f"{url}/health", timeout=5).raise_for_status()
        print("OK")
    except Exception as e:
        print(f"FAILED\n{e}")
        print("Start backend with: uvicorn main:app --host 0.0.0.0 --port 8000")
        sys.exit(1)


def print_summary(rows):
    print(f"\n{'='*58}")
    print(f"  {'Scenario':<12} {'Engine':<12} {'Mean WER':>9} {'Mean CER':>9} {'Avg Lat':>9} {'N':>4}")
    print(f"  {'-'*56}")
    for s in SCENARIOS:
        subset = [r for r in rows if r["scenario"] == s["name"] and r["wer"] is not None]
        if not subset:
            print(f"  {s['name']:<12} {s['engine']:<12} {'no results':>32}")
            continue
        print(
            f"  {s['name']:<12} {s['engine']:<12}"
            f" {mean(r['wer'] for r in subset)*100:>8.1f}%"
            f" {mean(r['cer'] for r in subset if r['cer'] is not None)*100:>8.1f}%"
            f" {mean(r['latency_s'] for r in subset):>8.3f}s"
            f" {len(subset):>4}"
        )

    failure = [r for r in rows if r["image"] == "blurry_failure_case.jpg"]
    if failure:
        print(f"\n  Failure case (blurry_failure_case.jpg):")
        for r in failure:
            wer = f"{r['wer']*100:.1f}%" if r["wer"] is not None else "n/a"
            cer = f"{r['cer']*100:.1f}%" if r["cer"] is not None else "n/a"
            print(f"    [{r['scenario']:<10}]  WER={wer:>7}  CER={cer:>7}  latency={r['latency_s']:.3f}s")
    print(f"{'='*58}\n")


def run(photos_dir, gt_path, url, output):
    if not gt_path.exists():
        print(f"Ground truth not found: {gt_path}")
        print("Run prepare_dataset.py first.")
        sys.exit(1)

    raw_gt = json.loads(gt_path.read_text(encoding="utf-8"))
    ground_truth = {name: parse_sroie_value(val) for name, val in raw_gt.items()}
    images = sorted(p for p in photos_dir.iterdir() if p.suffix.lower() in IMAGE_EXTS and p.name in ground_truth)

    if not images:
        print(f"No matching images in {photos_dir}")
        sys.exit(1)

    print(f"Images: {len(images)}  |  Scenarios: {[s['name'] for s in SCENARIOS]}")
    print(f"Output: {output}\n")
    check_backend(url)

    rows = []
    print(f"\n{'-'*58}")

    for img_path in images:
        b64 = encode(img_path)
        if not b64:
            continue

        tag = " [FAILURE CASE]" if img_path.name == "blurry_failure_case.jpg" else ""
        print(f"\n  {img_path.name}{tag}")

        for scenario in SCENARIOS:
            result, latency = call_evaluate(url, b64, ground_truth[img_path.name], scenario)
            wer = result.get("wer")
            cer = result.get("cer")
            status = result.get("status", "unknown")

            print(
                f"    [{scenario['name']:<10}]  "
                f"WER={f'{wer*100:.1f}%' if wer is not None else 'n/a':>7}  "
                f"CER={f'{cer*100:.1f}%' if cer is not None else 'n/a':>7}  "
                f"latency={latency:.3f}s  status={status}"
            )

            rows.append({
                "image": img_path.name,
                "scenario": scenario["name"],
                "engine": scenario["engine"],
                "fuzzy": scenario["fuzzy"],
                "wer": wer,
                "cer": cer,
                "latency_s": latency,
                "status": status,
                "detected_language": result.get("language", ""),
            })

    print(f"\n{'-'*58}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved → {output}")
    print_summary(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--photos", default="test_photos")
    parser.add_argument("--gt", default="test_photos/ground_truth.json")
    parser.add_argument("--url", default=BACKEND_URL)
    parser.add_argument("--output", default="evaluation_results.csv")
    args = parser.parse_args()
    run(Path(args.photos), Path(args.gt), args.url, Path(args.output))


if __name__ == "__main__":
    main()
