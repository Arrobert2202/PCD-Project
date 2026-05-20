# Baseline Comparison Plan (Repository-Compatible)

## Recommended baseline

**Baseline condition:** same backend with minimal processing path:
- `engine = paddleocr` (full-image OCR without custom region detector)
- `fuzzy = false`
- `lang = auto`

Rationale: this is the simplest in-repo condition closest to off-the-shelf OCR behavior while staying within implemented endpoints.

## Proposed system condition

**Proposed condition:** current default-rich pipeline:
- `engine = easyocr`
- `lang = auto`
- with/without `fuzzy=true` (report both)
- includes preprocessing + layout region detection + reading-order heuristic.

## Comparison tasks

1. Run batch OCR evaluation on identical dataset subset for both conditions.
2. Compare OCR quality (WER/CER/perfect/no-text).
3. Compare perceived navigability of blocks on sample documents (manual rubric).
4. Optionally compare per-image latency by logging timestamps in benchmark.

## Metrics

- Primary: WER, CER
- Secondary: perfect-match rate, no-text rate, average confidence (if computed), runtime latency
- Usability adjunct: block order usefulness score (manual 1–5)

## Result table templates

### Quantitative OCR

| Condition | Engine | Fuzzy | WER ↓ | CER ↓ | Perfect ↑ | No-text ↓ | N |
|---|---|---|---:|---:|---:|---:|---:|
| Baseline | paddleocr | false |  |  |  |  |  |
| Proposed | easyocr | false |  |  |  |  |  |
| Proposed+ | easyocr | true |  |  |  |  |  |

### Qualitative layout/navigation

| Document ID | Baseline readability (1-5) | Proposed readability (1-5) | Ordering errors | Notes |
|---|---:|---:|---:|---|
|  |  |  |  |  |

## How to avoid overstated claims

- Report confidence intervals or at least dataset size `N`.
- Separate OCR text accuracy from accessibility/usability outcomes.
- Explicitly state unsupported modalities (e.g., PDF) and evaluation limits.
- Use “improves on tested subset” wording, not universal claims.
