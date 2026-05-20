# Evaluation Readiness

## What can already be evaluated

- OCR text quality via WER/CER using `/evaluate` and `/evaluate/batch` (`backend/main.py`)
- Cross-engine comparison (`easyocr`, `tesseract`, `paddleocr`) via `benchmark.py --engines ...`
- Error/no-text rates from benchmark stats (`benchmark.py::compute_stats`)

## What cannot yet be reliably evaluated

- Accessibility effectiveness for visually impaired users (no task protocol/results found)
- Layout-understanding quality beyond bbox/read-order heuristics (no semantic layout metrics)
- Privacy outcomes (no policy controls, no audit checklist)
- Reproducible paper-ready benchmark package committed in-repo (datasets/ground truth not versioned in repo)

## Minimal evaluation package to add

1. Fixed, versioned evaluation subset (e.g., 50-150 images) with ground truth text.
2. Scripted run command and saved outputs (`results.json` + summary table CSV).
3. Per-engine report including WER/CER, no-text, runtime.
4. Small accessibility task test protocol (3-5 tasks, success rate/time/errors).
5. Failure-case appendix with representative hard examples.

## Proposed metrics

- OCR: WER, CER, perfect-match rate, no-text rate
- Layout usefulness: block-order correctness (manual rating), bbox coverage score (if annotations available)
- Runtime: median latency per document
- Accessibility: task success rate, task completion time, number of recovery actions, SUS-like questionnaire (if feasible)
- Safety: rate of low-confidence warnings triggered vs accepted outputs

## Proposed experiment table (template)

| Condition | Engine | Dataset split | WER ↓ | CER ↓ | Perfect ↑ | No-text ↓ | Median latency (s) ↓ | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|
| Baseline | Raw EasyOCR | Eval-v1 |  |  |  |  |  |  |
| Proposed | EasyOCR + preprocess + layout + optional fuzzy | Eval-v1 |  |  |  |  |  |  |
| Baseline | Raw Tesseract | Eval-v1 |  |  |  |  |  |  |
| Proposed | Tesseract + preprocess + post-process | Eval-v1 |  |  |  |  |  |  |
