# ChatGPT Handoff Summary

## What this repository currently appears to implement

A local-network OCR prototype with:
- Flutter mobile app for camera/upload input,
- Python FastAPI backend for OCR (EasyOCR/Tesseract/PaddleOCR),
- OCR result block visualization + TTS playback,
- evaluation endpoints and a Kaggle-driven benchmark script using WER/CER.

## Detected application name

- User-facing: **ReadDoc** (`README.md`, `flutter_app/lib/main.dart`, `flutter_app/lib/home_screen.dart`)
- Package/build naming still generic in places (`flutter_app`, iOS display name “Flutter App”).

## Current stack

- Backend: Python, FastAPI, OpenCV, EasyOCR/Tesseract/PaddleOCR, jiwer, lingua
- Frontend: Flutter (Dart), image_picker, file_picker, flutter_tts, http
- Evaluation: `benchmark.py` + Kaggle API

## Strongest parts

1. Multi-engine OCR support exposed through one API.
2. Structured OCR response (blocks + bounding boxes + full text).
3. Initial accessibility support (Semantics labels, TTS read-all and block-level reading).
4. Built-in quantitative evaluation hooks (WER/CER, batch evaluation, benchmark).

## Weakest parts

1. PDF support mismatch (UI allows PDF, backend rejects non-JPEG/PNG).
2. No formal privacy policy/retention control; debug image persistence risk.
3. No robust reproducible in-repo evaluation package with fixed ground truth.
4. No user-study evidence for visually impaired users.

## Biggest gaps vs Project 7 requirements

- Privacy analysis and safeguards not fully implemented/documented.
- Baseline comparison/report not committed as evidence.
- Layout/document understanding remains shallow (bbox + ordering heuristic only).
- IEEE paper materials/specification traceability missing.

## What evidence exists

- OCR/evaluation backend: `backend/main.py`, `backend/ocr_engine.py`, `backend/layout.py`, `backend/schemas.py`
- Accessibility/UI behavior: `flutter_app/lib/home_screen.dart`, `flutter_app/lib/ocr_result_screen.dart`, `flutter_app/lib/tts_service.dart`
- Evaluation automation: `benchmark.py`

## What is missing

- Reproducible labeled evaluation subset in repo
- Formal accessibility/usability evaluation protocol/results
- Privacy policy + data lifecycle controls
- IEEE-ready paper scaffold and final result figures/tables

## Top research questions to investigate next

1. Best baseline and fair comparison methodology for assistive OCR prototypes.
2. Robust reading-order/layout methods for mobile-captured mixed-layout docs.
3. Accessibility patterns for audio navigation and uncertainty communication.
4. Privacy-by-design patterns for sensitive document OCR systems.

## Recommended next actions

1. Fix immediate functional mismatch (PDF input path).
2. Remove/guard debug image persistence and document privacy behavior.
3. Build a fixed evaluation package and run baseline vs proposed comparisons.
4. Draft IEEE structure with requirement traceability and limitations.

## Exact files ChatGPT should inspect first

1. `/backend/main.py`
2. `/backend/ocr_engine.py`
3. `/backend/layout.py`
4. `/backend/preprocess.py`
5. `/flutter_app/lib/home_screen.dart`
6. `/flutter_app/lib/ocr_result_screen.dart`
7. `/flutter_app/lib/ocr_service.dart`
8. `/benchmark.py`
9. `/README.md`
10. `/docs/agent_analysis/*.md` (this package)
