# ChatGPT Handoff Summary

## What this repository appears to implement
A working prototype named **ReadDoc**: Flutter mobile app captures/uploads images, sends them to a local FastAPI backend, receives OCR text blocks with bounding boxes, and provides on-device TTS playback and block-level interaction.

## Current app name and stack
- **App name detected:** ReadDoc
- **Stack:** Flutter/Dart frontend + Python FastAPI backend + EasyOCR/Tesseract/PaddleOCR + OpenCV preprocessing + jiwer evaluation

## Strongest parts
- Multi-engine OCR backend with selectable engine/language/fuzzy options
- Block-level bbox output and UI overlay interaction
- Built-in evaluation endpoints and benchmark scripts (WER/CER)
- Existing sample data and prior evaluation CSV artifact

## Weakest parts
- No formal privacy policy; logs include raw OCR/ground-truth text
- PDF support mismatch (UI allows PDF; backend image-only)
- Accessibility is functional but still basic (no advanced navigation model/uncertainty narration)
- Reproducibility is fragile (tooling/setup not fully pinned; stale frontend test)

## Biggest gaps against Project 7
- Limited document understanding beyond OCR blocks (no semantic structuring/summarization)
- No formal accessibility usability evaluation protocol
- No rigorous baseline protocol/reporting package
- Missing IEEE paper scaffold/spec traceability in repo artifacts

## Evidence that exists
- Core pipeline: `backend/main.py`, `backend/preprocess.py`, `backend/layout.py`, `backend/ocr_engine.py`
- Accessibility UI/TTS: `flutter_app/lib/home_screen.dart`, `flutter_app/lib/ocr_result_screen.dart`, `flutter_app/lib/tts_service.dart`
- Evaluation tooling: `benchmark.py`, `benchmark_eval.py`, `evaluation_results.csv`, `test_photos/`

## Evidence missing or not found
- Explicit privacy/consent policy docs
- Structured layout understanding metrics/datasets
- User-study materials for visually impaired users
- IEEE manuscript/spec section files
- Robust reproducibility package (containerized or pinned full env)

## Top research questions to prioritize
1. Best baseline/proposed OCR evaluation protocol for accessible OCR projects
2. Effective audio navigation patterns for visually impaired document consumption
3. Practical layout-reading-order evaluation methods for scanned receipts/documents
4. Privacy-preserving design patterns for local/LAN OCR processing
5. How to frame realistic IEEE contributions for this implementation level

## Recommended next actions
1. Resolve PDF mismatch and logging privacy risk first.
2. Normalize dataset/ground-truth protocol and lock benchmark configuration.
3. Add confidence-aware accessible navigation improvements.
4. Build requirement-traceability table and paper skeleton with evidence links.
5. Run controlled baseline vs proposed experiments with reproducible scripts.

## Exact files ChatGPT should inspect first
1. `/home/runner/work/PCD-Project/PCD-Project/backend/main.py`
2. `/home/runner/work/PCD-Project/PCD-Project/backend/preprocess.py`
3. `/home/runner/work/PCD-Project/PCD-Project/backend/layout.py`
4. `/home/runner/work/PCD-Project/PCD-Project/backend/ocr_engine.py`
5. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/home_screen.dart`
6. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/ocr_result_screen.dart`
7. `/home/runner/work/PCD-Project/PCD-Project/benchmark_eval.py`
8. `/home/runner/work/PCD-Project/PCD-Project/benchmark.py`
9. `/home/runner/work/PCD-Project/PCD-Project/evaluation_results.csv`
10. `/home/runner/work/PCD-Project/PCD-Project/test_photos/ground_truth.json`
