# Repository Overview

## Snapshot
- **Repository name:** `Arrobert2202/PCD-Project`
- **Detected application name(s):** `ReadDoc` (UI title in `flutter_app/lib/main.dart`, app bar text in `flutter_app/lib/home_screen.dart`)
- **Detected technology stack:**
  - Backend: Python + FastAPI + Uvicorn (`backend/main.py`, `backend/requirements.txt`)
  - Mobile client: Flutter/Dart (`flutter_app/lib/*.dart`, `flutter_app/pubspec.yaml`)
  - OCR-related dependencies are declared but not wired in backend code (`backend/requirements.txt`)
- **Main entry points:**
  - Backend: `backend/main.py` (`FastAPI()` app with `/health`)
  - Flutter: `flutter_app/lib/main.dart` (`runApp(const App())`)
- **How project appears to run:** manual two-process setup (backend on laptop + Flutter app on phone), per `README.md`
- **Current artifact state:** mobile UI + TTS flow + network OCR request client exist; backend OCR endpoint is not implemented in current code

## Major files/folders

| Path | Purpose | Evidence | Notes |
|---|---|---|---|
| `/README.md` | Setup and claimed architecture | Sections “backend”, “flutter app”, “project structure” | Claims `eval/` and OCR pipeline; these are not present in current tree. |
| `/backend/main.py` | Backend API server | `FastAPI()` and `/health` route only | No `/ocr` route found. |
| `/backend/requirements.txt` | Python dependencies | FastAPI + OCR libs + jiwer listed | EasyOCR/Tesseract/OpenCV/jiwer are currently unused in backend code. |
| `/flutter_app/lib/main.dart` | Flutter app entry and theme | `MaterialApp(title: 'ReadDoc', home: HomeScreen)` | Dark theme mobile app. |
| `/flutter_app/lib/home_screen.dart` | Main UI and interaction flow | `_capture()`, `_showSettings()`, `Semantics`, `SemanticsService.announce` | Captures camera image, calls OCR service, reads text with TTS. |
| `/flutter_app/lib/ocr_service.dart` | Client for OCR API | `MultipartRequest('POST', BackendConfig.ocrEndpoint)` | Expects JSON with `status`, `engine`, `blocks`, `full_text`. |
| `/flutter_app/lib/tts_service.dart` | Text-to-speech wrapper | `FlutterTts`, `speak`, `setCompletionHandler` | Language hardcoded to `en-US`. |
| `/flutter_app/lib/config.dart` | Backend host/port config | `ocrEndpoint` and `healthEndpoint` getters | Uses plain HTTP local IP. |
| `/flutter_app/test/widget_test.dart` | Widget test scaffold | References `MyApp` | Inconsistent with current app class name `App`; likely failing/stale test. |
| `/flutter_app/android/app/src/main/AndroidManifest.xml` | Android app manifest | Activity declaration only | No explicit camera/internet permission in main manifest (debug/profile include internet). |
| `/flutter_app/ios/Runner/Info.plist` | iOS permissions/meta | `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription` | iOS has camera/photo usage text. |
| `/docs/agent_analysis/` | Analysis package folder | Created in this task | Contains evidence-based project assessment docs. |

## Dependency highlights
- **Backend declared:** `fastapi`, `uvicorn`, `python-multipart`, `easyocr`, `pytesseract`, `opencv-python`, `numpy`, `Pillow`, `jiwer`, `requests` (`backend/requirements.txt`)
- **Flutter declared:** `http`, `image_picker`, `flutter_tts` (`flutter_app/pubspec.yaml`)

## Validation checks observed in this environment
- `python3 -m py_compile backend/main.py` succeeds (run before docs edits).
- `flutter --version` failed (`command not found`) in this sandbox, so Flutter analyze/test could not be executed here.
- `python3 -m pytest -q` failed because `pytest` is not installed and no Python test setup is present.
