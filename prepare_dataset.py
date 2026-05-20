#!/usr/bin/env python3
"""
Download a small OCR dataset subset and prepare ground truth for benchmarking.
Usage: python prepare_dataset.py [--count 18] [--out test_photos] [--blur-radius 6]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from datasets import load_dataset
    from PIL import Image, ImageFilter
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install datasets pillow")
    sys.exit(1)


def get_image(sample):
    for key in ("image", "img", "scan"):
        val = sample.get(key)
        if val is None:
            continue
        if isinstance(val, Image.Image):
            return val.convert("RGB")
        if isinstance(val, dict):
            if val.get("bytes"):
                import io
                return Image.open(io.BytesIO(val["bytes"])).convert("RGB")
            if val.get("path") and Path(val["path"]).exists():
                return Image.open(val["path"]).convert("RGB")
    return None


def get_text(sample):
    if isinstance(sample.get("text"), str) and sample["text"].strip():
        return sample["text"].strip()
    if isinstance(sample.get("words"), list):
        return " ".join(w for w in sample["words"] if isinstance(w, str)).strip()
    if isinstance(sample.get("entities"), dict):
        parts = [v.strip() for v in sample["entities"].values() if isinstance(v, str) and v.strip()]
        if parts:
            return " ".join(parts)
    if isinstance(sample.get("ground_truth"), str):
        try:
            gt = json.loads(sample["ground_truth"])
            if isinstance(gt, dict):
                return " ".join(str(v) for v in gt.values() if v)
        except (json.JSONDecodeError, TypeError):
            pass
    return ""


DATASETS = [
    ("naver-clova-ix/cord-v2", None, "test"),
    ("nielsr/funsd-layoutlmv3", None, "test"),
    ("darentang/generated", "receipt", "train"),
]


def download(count):
    for hf_path, config, split in DATASETS:
        print(f"Trying {hf_path}...", end=" ", flush=True)
        try:
            ds = load_dataset(hf_path, config, split=split, trust_remote_code=True)
        except Exception as e:
            print(f"failed ({e})")
            continue

        pairs = []
        for sample in ds:
            img = get_image(sample)
            text = get_text(sample).strip()
            if img and text:
                pairs.append((img, text))
            if len(pairs) >= count:
                break

        if pairs:
            print(f"got {len(pairs)} samples")
            return pairs
        print("no valid samples")

    print("Could not download any dataset.")
    sys.exit(1)


def run(count, out_dir, blur_radius):
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {count} images...")
    pairs = download(count)

    ground_truth = {}
    blur_img = None
    blur_text = ""

    for idx, (img, text) in enumerate(pairs):
        name = f"sroie_{idx:03d}.jpg"
        img.save(out_dir / name, format="JPEG", quality=95)
        ground_truth[name] = text
        if idx == len(pairs) // 2:
            blur_img = img
            blur_text = text
        print(f"  {name}")

    if blur_img:
        blurry = blur_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        blurry.save(out_dir / "blurry_failure_case.jpg", format="JPEG", quality=95)
        ground_truth["blurry_failure_case.jpg"] = blur_text
        print(f"  blurry_failure_case.jpg (blur radius={blur_radius})")

    gt_path = out_dir / "ground_truth.json"
    gt_path.write_text(json.dumps(ground_truth, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nDone. {len(ground_truth)} entries saved to {gt_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=18)
    parser.add_argument("--out", default="test_photos")
    parser.add_argument("--blur-radius", type=int, default=6)
    args = parser.parse_args()
    run(args.count, Path(args.out), args.blur_radius)


if __name__ == "__main__":
    main()
