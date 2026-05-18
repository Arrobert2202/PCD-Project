# Evaluation Readiness

## What can already be evaluated
- **UI interaction flow (without OCR backend):** scan action, loading/error transitions, TTS invocation paths (`home_screen.dart`).
- **Network error handling quality:** timeout and non-200 behavior in `ocr_service.dart`.
- **Basic accessibility semantics presence:** `Semantics` wrappers and announcements.

## What cannot yet be evaluated
- OCR quality (CER/WER/accuracy): backend OCR route is missing.
- Layout extraction quality: no layout implementation.
- Document understanding/summarization quality: no implementation.
- Baseline vs proposed comparisons: no baseline scripts/results.
- End-to-end latency under real OCR workload: no processing backend.

## Minimal evaluation package to add next
1. Small fixed dataset (e.g., 20–50 representative document images) with ground truth text.
2. Backend `/ocr` implementation with deterministic JSON schema.
3. Evaluation script computing CER/WER (and optional block-order correctness).
4. Baseline condition (raw OCR output without layout navigation).
5. Result tables + failure examples committed in `eval/`.

## Proposed metrics
- OCR text quality: CER, WER.
- Structural quality: block order accuracy (manual rubric), block detection precision/recall (if boxes added).
- Accessibility usability: task completion rate, time-to-find target info, subjective workload (e.g., short Likert survey).
- System performance: median/95th percentile processing time per page.

## Proposed experiment table (template)

| Condition | Dataset split | CER | WER | Block order score | Task completion (%) | Median latency (s) | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Baseline OCR only | Test set A |  |  | N/A |  |  |  |
| Proposed system | Test set A |  |  |  |  |  |  |
| Proposed + navigation aids | Test set A |  |  |  |  |  |  |

## Evidence limitations
- README references evaluation components not present in current tree.
- `jiwer` dependency suggests intent, not realized evaluation pipeline.
