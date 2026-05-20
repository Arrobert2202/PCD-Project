# Architecture Reconstruction (Observed)

## Observed architecture

A **client-server local OCR system**:
- Flutter client captures/selects document images and sends them to backend over HTTP.
- Python FastAPI backend preprocesses image, runs selected OCR engine, structures output into text blocks, and returns text + bounding boxes.
- Optional evaluation path computes WER/CER against provided ground truth text.

**Primary evidence:** `flutter_app/lib/home_screen.dart`, `flutter_app/lib/ocr_service.dart`, `backend/main.py`, `backend/ocr_engine.py`, `backend/preprocess.py`, `backend/layout.py`.

## Frontend/backend split

- **Frontend:** Flutter (`flutter_app/lib/*`)
  - Input: camera/file picker
  - Controls: OCR engine/language/fuzzy options
  - Output UI: image with overlayed blocks + text block list + TTS
- **Backend:** FastAPI (`backend/main.py`)
  - Endpoints: `/health`, `/ocr`, `/ocr/batch`, `/evaluate`, `/evaluate/batch`
  - Engine abstraction: EasyOCR/Tesseract/PaddleOCR

## Data flow

```mermaid
flowchart LR
A[User captures or picks file] --> B[Flutter HomeScreen]
B --> C[OcrService POST /ocr]
C --> D[FastAPI backend]
D --> E[Preprocess image]
E --> F{Engine}
F -->|easyocr| G[Layout detect + crop OCR]
F -->|tesseract| H[Tesseract OCR]
F -->|paddleocr| I[PaddleOCR OCR]
G --> J[Blocks + full_text]
H --> J
I --> J
J --> K[Optional fuzzy correction]
K --> L[JSON OCRResponse]
L --> M[Flutter OcrResultScreen]
M --> N[TTS read-all / read-block]
```

## Processing pipeline (backend view)

```mermaid
flowchart TD
R[Request image base64] --> D1[_decode_image: validate format and size]
D1 --> P1[preprocess_image: upscale + deskew]
P1 --> O1[_run_engine]
O1 --> O2[raw OCR tuples text/conf/bbox]
O2 --> L1[detect_language when lang=auto]
L1 --> B1[build TextBlock list + bbox remap]
B1 --> F1{fuzzy?}
F1 -->|yes| F2[apply_fuzzy_matching]
F1 -->|no| OUT
F2 --> OUT[OCRResponse]
```

## Storage behavior

- Request image bytes are processed in memory for OCR flow.
- **But** debug images are written to disk in `backend/debug/` via `_dbg` and `dbg_boxes` (`backend/preprocess.py`).
- SymSpell dictionaries are downloaded and cached under `backend/symspell_dicts/` (`backend/fuzzy.py`).

## Dependency graph (high level)

- `backend/main.py` depends on: `schemas.py`, `preprocess.py`, `layout.py`, `ocr_engine.py`, `fuzzy.py`, `jiwer`, `lingua`
- `ocr_engine.py` lazily imports OCR libraries per engine.
- Flutter UI depends on `ocr_service.dart` and `tts_service.dart`.

## External services and runtime assumptions

- No backend database detected.
- Optional external dependencies:
  - GitHub raw content for SymSpell frequency dictionaries (`backend/fuzzy.py`)
  - Kaggle API for benchmark dataset download (`benchmark.py`)
- Runtime assumptions:
  - Backend reachable on local network IP/port configured in app (`flutter_app/lib/config.dart` + settings dialog in `home_screen.dart`)
  - Tesseract executable availability is system-dependent (`backend/ocr_engine.py::_configure_tesseract`)

## Uncertain/needs verification

- Full cross-platform camera/file permission behavior in Android without explicit manifest permissions in committed `AndroidManifest.xml` (plugin merge may supply behavior).
- Production deployment model beyond local LAN prototype not found.
