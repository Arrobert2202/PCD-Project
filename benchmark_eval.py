#!/usr/bin/env python3
"""
Evaluate OCR backend on prepared dataset and export results to CSV.
Usage: python benchmark_eval.py [--photos test_photos] [--gt test_photos/ground_truth.json]
"""

import argparse
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
]

CSV_COLUMNS = ["image", "scenario", "engine", "fuzzy", "wer", "cer", "latency_s", "status", "detected_language"]


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

    ground_truth = json.loads(gt_path.read_text(encoding="utf-8"))
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
