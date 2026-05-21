# Architecture Reconstruction

## Observed architecture
A **2-tier local system** is implemented:
1. **Flutter client** captures/selects images and sends base64 payloads to backend (`flutter_app/lib/ocr_service.dart`)
2. **FastAPI backend** preprocesses image, runs selected OCR engine, returns text blocks and full text (`backend/main.py`)

## Frontend/backend split
- **Frontend:** `flutter_app/lib/*`
- **Backend:** `backend/*`
- **Evaluation utilities:** repository root (`benchmark.py`, `benchmark_eval.py`, `prepare_dataset.py`)

## Reconstructed runtime flow
```mermaid
flowchart LR
  User --> UI[Flutter UI\nhome_screen.dart]
  UI --> OCRSvc[ocr_service.dart\nHTTP POST /ocr]
  OCRSvc --> API[FastAPI backend\nbackend/main.py]
  API --> Pre[preprocess.py\nscale + deskew]
  API -->|easyocr| Layout[layout.py\ntext regions + reading order]
  API --> Engines[ocr_engine.py\nEasyOCR/Tesseract/PaddleOCR]
  Engines --> API
  API --> Resp[OCRResponse\nblocks + full_text + language]
  Resp --> ResultUI[ocr_result_screen.dart\noverlays + list]
  ResultUI --> TTS[tts_service.dart\nflutter_tts]
```

## Backend processing pipeline (from code)
```mermaid
flowchart TD
  A[Input base64 image] --> B[_decode_image\nJPEG/PNG, <=10MB]
  B --> C[preprocess_image]
  C --> D{engine}
  D -->|easyocr| E[detect_text_regions]
  E --> F[run_easyocr per bbox]
  D -->|tesseract| G[run_tesseract full image]
  D -->|paddleocr| H[run_paddleocr full image]
  F --> I[build blocks]
  G --> I
  H --> I
  I --> J[detect_language post-hoc if auto]
  J --> K{fuzzy?}
  K -->|yes| L[apply_fuzzy_matching]
  K -->|no| M[compose full_text]
  L --> M
  M --> N[OCRResponse]
```

## Storage behavior
- **Persistent logs:** `backend/logs/backend.log` via rotating handler (`backend/main.py`)
- **No database layer found** (not found)
- **Optional dictionary cache:** `backend/symspell_dicts/` created dynamically (`backend/fuzzy.py`)
- **Test/eval artifacts:** `evaluation_results.csv`, `test_photos/*`

## External services/dependencies
- OCR libraries/models: EasyOCR, PaddleOCR, Tesseract local runtime
- Dataset sources: Kaggle API (`benchmark.py`), Hugging Face datasets (`prepare_dataset.py`)
- Dictionary download: GitHub raw FrequencyWords (`backend/fuzzy.py`)

## Runtime assumptions
- Backend reachable on local network by mobile device (`flutter_app/lib/config.dart`, `README.md`)
- Tesseract executable/language packs installed on host for tesseract path (`backend/ocr_engine.py`, `docs/languages.md`)
- GPU availability implicitly assumed for EasyOCR (`gpu=True` in `get_easyocr_reader`)

## Uncertain parts
- PDF handling appears selectable in UI but unsupported by backend image decoder; true intended PDF flow is uncertain.
- README references `eval/` folder but current repository uses root-level scripts; possible stale documentation.
