# ChatGPT Handoff Summary

## What this repository currently appears to implement
- A **Flutter mobile frontend** for capturing a document photo and attempting OCR processing through a backend endpoint.
- **Text-to-speech readout** and basic accessibility semantics/announcements in the app.
- A **minimal FastAPI backend** with only a `/health` endpoint (no OCR route currently implemented).

## Detected app name
- Primary detected name: **ReadDoc** (`flutter_app/lib/main.dart`, `flutter_app/lib/home_screen.dart`)

## Current stack
- Backend: Python, FastAPI, Uvicorn.
- Frontend: Flutter/Dart with `image_picker`, `http`, `flutter_tts`.
- Declared but unused backend OCR/eval deps: EasyOCR, pytesseract, OpenCV, jiwer.

## Strongest parts
- Clean mobile UX skeleton with explicit app states (`ready/loading/playing/error`).
- TTS integration and semantic announcements for status/error updates.
- Client API model already defines expected structured OCR response schema (`blocks`, `full_text`).

## Weakest parts
- Backend OCR endpoint `/ocr` is missing.
- No implemented evaluation pipeline or dataset artifacts.
- Stale/likely broken default Flutter test.
- README claims exceed current repository contents (e.g., `eval/` and full OCR pipeline claims).

## Biggest gaps vs Project 7 requirements
1. OCR accuracy evaluation (no CER/WER scripts/results despite dependency hints).
2. Layout extraction and navigable structure (client model exists, backend implementation missing).
3. Accessible navigation beyond monolithic speech output.
4. Privacy/ethics implementation (consent, retention policy, secure transport posture).
5. Baseline comparison and IEEE-spec traceability artifacts.

## Evidence that exists
- `backend/main.py`: only `/health` route.
- `flutter_app/lib/ocr_service.dart`: expects `POST /ocr` JSON with blocks/full text.
- `flutter_app/lib/home_screen.dart`: camera capture, error handling, semantics announcements, TTS trigger.
- `flutter_app/lib/tts_service.dart`: English TTS configuration and playback.
- `README.md`: setup instructions and claims about OCR/eval (partly unmatched).

## What is missing (not found)
- Implemented OCR backend route and processing pipeline.
- Evaluation directory/scripts/results.
- Baseline implementation/results.
- Paper/report artifacts (`.tex`, report docs, requirement traceability).
- Privacy policy/consent flow and explicit data handling policy.

## Top research questions to prioritize
1. Best lightweight OCR+layout stack for mobile-captured images under project constraints.
2. Evidence-based audio navigation design patterns for visually impaired users.
3. Minimal but rigorous baseline/evaluation protocol for course-scale accessible OCR research.
4. Privacy-by-design and ethics reporting standards for assistive document AI.

## Recommended next actions
1. Implement `/ocr` endpoint with stable response schema.
2. Add `eval/` package with dataset subset + CER/WER script + baseline condition.
3. Add block-level navigation UI and uncertainty messaging.
4. Reconcile README with actual implementation and reproducibility instructions.
5. Build IEEE paper skeleton with requirement IDs and traceability table.

## Exact files ChatGPT should inspect first
1. `/home/runner/work/PCD-Project/PCD-Project/backend/main.py`
2. `/home/runner/work/PCD-Project/PCD-Project/backend/requirements.txt`
3. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/home_screen.dart`
4. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/ocr_service.dart`
5. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/tts_service.dart`
6. `/home/runner/work/PCD-Project/PCD-Project/flutter_app/lib/config.dart`
7. `/home/runner/work/PCD-Project/PCD-Project/README.md`
8. `/home/runner/work/PCD-Project/PCD-Project/docs/agent_analysis/*.md`
