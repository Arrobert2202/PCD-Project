# Baseline Comparison Plan

## Recommended baseline (based on current repo)
**Baseline condition:** `tesseract`, `fuzzy=false`, fixed language (`en`) using existing `/evaluate` flow.
- Evidence: `benchmark_eval.py::SCENARIOS` already defines a baseline-like scenario.

## Proposed system condition(s)
- **Proposed-1:** `easyocr`, `fuzzy=true`, `fuzzer=symspell`, `lang=auto`
- **Proposed-2:** `paddleocr`, `fuzzy=false`, `lang=auto`
- These are already close to existing repository scenarios (`benchmark_eval.py`).

## Comparison tasks
1. Receipt/document OCR transcription quality on fixed test split
2. Robustness on blurred sample (`blurry_failure_case.jpg`)
3. Latency comparison per engine/scenario
4. Optional: block-level navigation usefulness (time to find a target item in OCR output)

## Metrics
- Primary: Mean WER, Mean CER
- Secondary: no-text rate, timeout/error rate, perfect-match rate, latency (mean/p90)
- Optional accessibility metric: time to locate target phrase using UI navigation

## Result table templates

### Quantitative OCR comparison
| Scenario | Engine | Fuzzy | Mean WER | Mean CER | Perfect matches | No-text count | Mean latency (s) | p90 latency (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Baseline | tesseract | off |  |  |  |  |  |  |
| Proposed-1 | easyocr | on |  |  |  |  |  |  |
| Proposed-2 | paddleocr | off |  |  |  |  |  |  |

### Failure-case slice
| Image | Scenario | Status | WER | CER | Latency (s) | Observed failure pattern |
|---|---|---|---:|---:|---:|---|
| blurry_failure_case.jpg | Baseline |  |  |  |  |  |
| blurry_failure_case.jpg | Proposed-1 |  |  |  |  |  |
| blurry_failure_case.jpg | Proposed-2 |  |  |  |  |  |

## How to avoid overstated claims
- Use **fixed dataset split** and report full sample counts.
- Report both improvements and regressions (do not cherry-pick best samples).
- Separate OCR quality claims from accessibility claims unless user-study evidence exists.
- Explicitly state limitations: image-only pipeline, no full PDF parser, language-dependent behavior.
- Treat language auto-detection as auxiliary metadata, not proof of multilingual OCR quality.
