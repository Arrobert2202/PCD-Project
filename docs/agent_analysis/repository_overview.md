# Repository Overview

## Identity
- **Repository name:** `Arrobert2202/PCD-Project`
- **Detected application name:** **ReadDoc** (from `README.md`, `flutter_app/lib/main.dart`, `flutter_app/lib/home_screen.dart`)
- **Current artifact:** Mobile OCR client (Flutter) + local OCR/evaluation backend (FastAPI)

## Detected technology stack
- **Frontend:** Flutter/Dart (`flutter_app/lib/*.dart`)
- **Backend API:** FastAPI + Pydantic (`backend/main.py`, `backend/schemas.py`)
- **OCR/document processing:** EasyOCR, Tesseract, PaddleOCR, OpenCV (`backend/ocr_engine.py`, `backend/layout.py`, `backend/preprocess.py`)
- **Evaluation:** jiwer (WER/CER), benchmark scripts (`backend/main.py`, `benchmark.py`, `benchmark_eval.py`)
- **Dataset tooling:** Hugging Face `datasets`, Kaggle API (`prepare_dataset.py`, `benchmark.py`)

## Main entry points
- Backend server: `backend/main.py` (`app = FastAPI()`, endpoints `/ocr`, `/evaluate`)
- Mobile app: `flutter_app/lib/main.dart` (`runApp(const App())`)
- Evaluation scripts: `benchmark.py`, `benchmark_eval.py`

## How project appears to be run
- Backend startup via uvicorn (`README.md`): `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- Flutter startup (`README.md`): `flutter pub get`, then `flutter run --release`
- Device/backend linking via editable host config (`flutter_app/lib/config.dart`)

## Major files/folders

| Path | Purpose | Evidence | Notes |
|---|---|---|---|
| `/README.md` | Setup + project usage | Run commands and architecture summary in sections “backend” and “flutter app” | Mentions `eval/` folder, but no such folder currently found |
| `/backend/main.py` | API routes + OCR orchestration + evaluation metrics | Endpoints `/health`, `/ocr`, `/ocr/batch`, `/evaluate`, `/evaluate/batch` | Core backend control flow lives in `_process_image` |
| `/backend/preprocess.py` | Image preprocessing and bbox coordinate transform | `preprocess_image`, `_normalize_scale`, `_deskew`, `PreprocessTransform.bbox_to_original` | No CLAHE/denoise despite Postman description claiming both |
| `/backend/layout.py` | Text-region detection + reading-order sorting | `detect_text_regions`, `sort_reading_order` | Used only for EasyOCR path |
| `/backend/ocr_engine.py` | OCR engine wrappers (EasyOCR/Tesseract/PaddleOCR) | `run_easyocr`, `run_tesseract`, `run_paddleocr` | EasyOCR forced `gpu=True` |
| `/backend/fuzzy.py` | Optional fuzzy/spell post-processing | `apply_fuzzy_matching` | Downloads SymSpell dictionaries from GitHub at runtime |
| `/backend/schemas.py` | Request/response models | `OCRRequest`, `EvaluateRequest`, `BatchEvaluateResponse` | Strong contract for API payloads |
| `/backend/requirements.txt` | Python dependencies | OCR, API, evaluation packages listed | Includes heavy dependencies (paddlepaddle) |
| `/flutter_app/lib/home_screen.dart` | Main UI, camera/file input, settings, options | `_captureFromCamera`, `_pickFromFiles`, `_showSettings` | Allows `pdf` selection but downstream pipeline expects image bytes |
| `/flutter_app/lib/ocr_service.dart` | Backend HTTP client + upload resizing | `processBytes`, `_prepareOcrUploadBytes` | Sends only base64 image data to `/ocr` |
| `/flutter_app/lib/ocr_result_screen.dart` | OCR output visualization + TTS playback | `_buildImageOverlay`, `_readBlock`, `_toggleReadAll` | Tap-by-bbox reading is implemented |
| `/flutter_app/lib/tts_service.dart` | Text-to-speech wrapper | `initialize`, `speak`, `stop` | Hardcoded `en-US` language |
| `/benchmark.py` | Kaggle dataset benchmarking against backend | `download_dataset`, `run_evaluation`, `compute_stats` | Supports multi-engine comparison |
| `/benchmark_eval.py` | Local test set benchmark + CSV export | `SCENARIOS`, `run`, `print_summary` | Includes baseline/optimized scenarios |
| `/prepare_dataset.py` | Build local test set + failure case | `download`, `run` | Adds `blurry_failure_case.jpg` intentionally |
| `/test_photos/` | Test images + ground truth | `ground_truth.json` and image set | Ground-truth value format is non-trivial concatenated literals |
| `/evaluation_results.csv` | Saved evaluation run output | WER/CER/latency rows per scenario | Indicates prior experiments were executed |
| `/docs/languages.md` | Language support matrix | Table of OCR/fuzzy support | Contains environment-specific claims that may not generalize |

## Validation command availability observed
- `python3 -m pytest` in `backend/` failed: `No module named pytest`
- `flutter analyze` failed: `flutter: command not found`
- `flutter test` failed: `flutter: command not found`

(Commands attempted in this environment; may differ on a fully provisioned local machine.)
