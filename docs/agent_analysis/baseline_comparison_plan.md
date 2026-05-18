# Baseline Comparison Plan (Based on Current Repository)

## Recommended baseline
**Baseline:** raw OCR text read aloud as one unstructured block (no layout navigation).

Rationale: this is the simplest valid comparison aligned with current client behavior (single `full_text` TTS output).

## Proposed system condition
- OCR with structured `blocks` and reading-order metadata.
- Accessible navigation controls (next/previous/repeat block).
- Confidence-aware alerts for uncertain segments.

## Comparison tasks
1. Locate a specific field (e.g., invoice total/date).
2. Read a paragraph from multi-block layout.
3. Verify a critical numeric value.
4. Resume reading after interruption.

## Metrics
- Task completion rate.
- Task completion time.
- Error rate (wrong value reported).
- Number of navigation actions.
- User-rated ease/confidence.
- OCR quality (CER/WER) for underlying text extraction.

## Result table templates

### Quantitative
| Task | Condition | Success (%) | Median time (s) | Error rate (%) | Mean actions | Notes |
|---|---|---:|---:|---:|---:|---|
| Field lookup | Baseline |  |  |  |  |  |
| Field lookup | Proposed |  |  |  |  |  |
| Paragraph reading | Baseline |  |  |  |  |  |
| Paragraph reading | Proposed |  |  |  |  |  |

### OCR quality
| Condition | CER | WER | Sample count | Notes |
|---|---:|---:|---:|---|
| Baseline OCR |  |  |  |  |
| Proposed OCR pipeline |  |  |  |  |

## How to avoid overstated claims
- Report only measured outcomes from repository-supported features.
- Separate **implemented** vs **planned** features in all figures/tables.
- Include failure cases and confidence intervals where possible.
- Avoid claiming accessibility benefit without user-task evidence.
