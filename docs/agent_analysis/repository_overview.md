# Repository Overview

- **Repository name:** `Arrobert2202/PCD-Project`
- **Detected application name(s):**
  - **ReadDoc** (user-facing name in UI/README) — `README.md`, `flutter_app/lib/main.dart`, `flutter_app/lib/home_screen.dart`
  - **flutter_app** (package/build name) — `flutter_app/pubspec.yaml`, `flutter_app/android/app/src/main/AndroidManifest.xml`
- **Detected technology stack:**
  - Backend: Python + FastAPI + Uvicorn + OpenCV + OCR engines (EasyOCR/Tesseract/PaddleOCR)
  - Mobile: Flutter (Dart), HTTP client, file/image picker, TTS
  - Evaluation: Python benchmark script using Kaggle datasets + WER/CER (`jiwer`)

## Main entry points

- `backend/main.py` — FastAPI app and OCR/evaluation endpoints
- `flutter_app/lib/main.dart` — Flutter app root
- `benchmark.py` — command-line benchmark/evaluation runner

## Main dependencies (detected)

- Backend (`backend/requirements.txt`): `fastapi`, `uvicorn`, `easyocr`, `pytesseract`, `paddleocr`, `opencv-python-headless`, `lingua-language-detector`, `symspellpy`, `pyspellchecker`, `jiwer`, `kaggle`
- Flutter (`flutter_app/pubspec.yaml`): `http`, `image_picker`, `file_picker`, `flutter_tts`

## How the project appears to be run

- Backend startup in README:
  - `cd backend`
  - create/activate venv
  - `pip install -r requirements.txt`
  - `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (`README.md`)
- Flutter app startup in README:
  - `cd flutter_app`
  - `flutter pub get`
  - `flutter run --release` (+ iOS `pod install`) (`README.md`)
- Benchmark:
  - `python benchmark.py ...` against running backend (`benchmark.py`)

## Current artifact (inferred)

A local-network OCR prototype for visually impaired users consisting of:
1. a Flutter mobile front-end (capture/upload + TTS + selectable text blocks), and
2. a Python backend OCR API with multiple OCR engines and basic quantitative evaluation endpoints.

## Major files/folders

| Path | Purpose | Evidence | Notes |
|---|---|---|---|
| `/README.md` | Setup and high-level description | Declares “ReadDoc — OCR Document Reader”; backend+Flutter run steps | Mentions `eval/` folder that is not present in tree (inconsistency) |
| `/backend/main.py` | API endpoints and OCR/evaluation orchestration | `@app.post('/ocr')`, `@app.post('/evaluate')`, `_process_image` | Core server logic and response shaping |
| `/backend/ocr_engine.py` | OCR engine adapters | `run_easyocr`, `run_tesseract`, `run_paddleocr` | Multi-engine support implemented |
| `/backend/layout.py` | Text-region detection and reading-order sorting | `detect_text_regions`, `sort_reading_order` | Used only by EasyOCR path |
| `/backend/preprocess.py` | Preprocessing + coordinate transform | `preprocess_image`, `PreprocessTransform` | Writes debug images via `_dbg`/`dbg_boxes` |
| `/backend/schemas.py` | API schema contracts | `OCRRequest`, `OCRResponse`, `EvaluateResponse` | Defines engine/lang/fuzzy fields |
| `/backend/fuzzy.py` | Post-OCR spell-correction | `apply_fuzzy_matching` | Downloads dictionaries from GitHub on demand |
| `/backend/requirements.txt` | Backend dependency lock-ish file | pinned versions for most packages | `numpy` is ranged, not fully pinned |
| `/flutter_app/lib/main.dart` | Flutter app bootstrapping | `MaterialApp(title: 'ReadDoc')` | Home screen is `HomeScreen` |
| `/flutter_app/lib/home_screen.dart` | Capture/upload flow and options UI | image/file picking, settings, semantics announcements | Allows `.pdf` pick but backend supports only PNG/JPEG |
| `/flutter_app/lib/ocr_service.dart` | Backend API client | POST to `BackendConfig.ocrEndpoint` | Network timeout and error wrapping |
| `/flutter_app/lib/ocr_result_screen.dart` | OCR result visualization + TTS navigation | bounding-box overlays, per-block read, read-all | Accessible labels added for key controls |
| `/flutter_app/lib/tts_service.dart` | TTS wrapper | `FlutterTts` init/speak/stop | Hard-coded `en-US` availability check |
| `/benchmark.py` | Dataset benchmark + metrics reporting | Kaggle download + `/evaluate/batch` calls + stats | Provides baseline-ready evaluation workflow |
| `/test_photos/` | Sample local test images | multiple `.png/.jpg` files | No paired committed ground-truth files found |
| `/docs/languages.md` | Declared language support matrix | table by OCR engine/fuzzer | Some notes appear machine/user-environment specific |
| `/OCR_Backend.postman_collection.json` | API manual test collection | requests for `/health`, `/ocr`, `/evaluate` | Description claims preprocessing steps not fully present in code |
