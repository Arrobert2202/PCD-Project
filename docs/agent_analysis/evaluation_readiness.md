# Evaluation Readiness

## What can already be evaluated
- OCR text accuracy against reference text via **WER/CER** (`/evaluate`, `/evaluate/batch` in `backend/main.py`)
- Engine comparison across EasyOCR/Tesseract/PaddleOCR (`benchmark.py`, `benchmark_eval.py`)
- Basic latency per request (`benchmark_eval.py` stores `latency_s`)
- Failure-case behavior on intentionally blurred sample (`prepare_dataset.py`, `benchmark_eval.py`)

## What cannot yet be evaluated reliably
- Layout quality metrics (IoU/F1 for block detection, reading order accuracy): no standardized labeled layout benchmark implemented
- Accessibility usability outcomes (task completion, SUS/UEQ, blind/low-vision user study): no protocol found
- Privacy/security outcomes: no measurable policy controls or audit checks
- Reproducible benchmark execution in this environment (missing `flutter`, missing `pytest`, heavyweight OCR setup)

## Minimal evaluation package to add next
1. **Pinned dataset manifest** (source, split IDs, license, checksums)
2. **Normalized ground-truth schema** (avoid concatenated literal format in `ground_truth.json`)
3. **Single command evaluation script** producing:
   - per-engine metrics table
   - aggregate confidence/latency stats
   - failure-case appendix
4. **Layout micro-benchmark** (small manually labeled set with bbox + reading-order target)
5. **Accessibility task protocol** (3-5 tasks, completion time/errors, subjective ratings)

## Proposed metrics
- **OCR accuracy:** WER, CER, perfect-line rate, no-text rate
- **Layout quality:** bbox precision/recall/F1, reading-order Kendall tau (or sequence accuracy)
- **Runtime:** mean/median latency, p90 latency, memory footprint (if possible)
- **Accessibility:** task completion rate, task time, user confidence score, error recovery rate
- **Robustness:** blur/noise/rotation degradation curves

## Proposed experiment table template

| Condition | Engine | Fuzzy | Language mode | Dataset split | Mean WER | Mean CER | No-text rate | p90 latency (s) | Notes |
|---|---|---|---|---|---:|---:|---:|---:|---|
| Baseline | tesseract | off | en | fixed-test-v1 |  |  |  |  |  |
| Proposed A | easyocr | on (symspell) | auto | fixed-test-v1 |  |  |  |  |  |
| Proposed B | paddleocr | off | auto | fixed-test-v1 |  |  |  |  |  |

## Evidence pointers
- Evaluation endpoints and metrics: `backend/main.py`
- Benchmark execution: `benchmark.py`, `benchmark_eval.py`
- Existing result artifact: `evaluation_results.csv`
- Dataset prep flow: `prepare_dataset.py`, `test_photos/ground_truth.json`
