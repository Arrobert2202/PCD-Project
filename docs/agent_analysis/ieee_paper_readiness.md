# IEEE Paper Readiness Assessment

## Possible title (based on actual repo)

**“ReadDoc: A Local OCR and Audio-Assisted Document Reader with Multi-Engine Evaluation”**

## Abstract skeleton

1. **Problem:** visually impaired users need accessible document text extraction and navigation.
2. **System:** Flutter mobile client + local FastAPI OCR backend with EasyOCR/Tesseract/PaddleOCR.
3. **Method:** preprocessing, optional layout-based region OCR, optional fuzzy correction, TTS navigation.
4. **Evaluation:** WER/CER via benchmark and `/evaluate` endpoints.
5. **Findings (to fill):** comparative engine performance + accessibility observations.
6. **Limitations:** PDF support mismatch, limited reproducible packaged datasets, privacy policy gaps.

## Keywords

OCR, accessibility, visually impaired users, document understanding, text-to-speech, FastAPI, Flutter, WER, CER

## Likely contribution statement

- A working local OCR prototype integrating multi-engine OCR and mobile TTS block navigation.
- A practical evaluation pipeline (WER/CER) across engines.
- An accessible interaction design starting point (semantics labels + block-level audio reading).

## Missing evidence before IEEE-ready submission

- Formal user study/usability results
- Stable benchmark dataset protocol and reproducible result package
- Explicit privacy/ethics methodology
- Clear layout-understanding evaluation beyond OCR accuracy

## Required figures

1. System architecture diagram (mobile client ↔ backend OCR pipeline)
2. OCR processing pipeline flowchart
3. Result-screen interaction diagram (bbox overlays + list + TTS flow)
4. Engine comparison chart (WER/CER)

## Required tables

1. Requirements traceability table (REQ IDs)
2. Dataset composition table
3. Engine comparison metrics table
4. Failure-case taxonomy table

## Integrated specification section draft

| ID | Requirement | Priority | Verification method | Current evidence | Missing evidence |
|---|---|---|---|---|---|
| REQ-01 | Accept image document input from mobile device | high | Functional test (camera/upload) | `home_screen.dart` capture/upload + `/ocr` | Need test report artifacts |
| REQ-02 | Extract text with OCR and return structured blocks | high | API contract test | `backend/main.py`, `schemas.py` blocks/full_text | Need automated integration tests |
| REQ-03 | Support at least one OCR baseline and one improved condition | high | Benchmark comparison run | `benchmark.py --engines` | Need committed benchmark results |
| REQ-04 | Provide navigable output for visually impaired users | high | Task-based usability test | TTS + block interactions in result screen | No user study protocol/results |
| REQ-05 | Provide accessible UI cues and announcements | high | Accessibility audit checklist | `Semantics` and `SemanticsService.announce` usage | No formal audit evidence |
| REQ-06 | Handle privacy of captured documents | high | Policy + technical inspection | local processing orientation, input validation | No retention/deletion policy; debug write risk |
| REQ-07 | Evaluate OCR quality quantitatively | high | WER/CER script and report | `/evaluate*` endpoints + `benchmark.py` | No reproducible dataset subset in repo |
| REQ-08 | Ensure reproducibility of experiments | high | Re-run protocol from clean env | README + requirements/pubspec | Missing pinned full environment + expected outputs |
| REQ-09 | Document limitations and threats to validity | medium | Paper section review | Some code-level evidence of limits | Not yet written in paper materials |

## Limitations and threats to validity (current)

- Dataset variability and annotation quality if using arbitrary Kaggle downloads.
- No controlled user evaluation with target population.
- Engine behavior can vary by hardware/model downloads.
- PDF/document-type coverage incomplete.
- Potential privacy risk from debug image persistence.
