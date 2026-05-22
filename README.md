# ReadDoc — Accessible OCR App

Mobile OCR system built with Flutter + FastAPI, designed for visually impaired users. You take a photo of a document, the backend extracts the text, and the app reads it aloud via TTS.

Everything runs on your local network — no cloud, no data leaves your Wi-Fi.

---

## How it works

```
┌─────────────────────┐        Wi-Fi (LAN only)       ┌──────────────────────────────┐
│   Flutter Client    │  ──────────────────────────►  │     FastAPI Backend          │
│   (Android / iOS)   │                               │                              │
│                     │  ◄──────────────────────────  │  Layout detection            │
│  Camera → HTTP POST │        JSON response           │  EasyOCR / Tesseract         │
│  TTS playback       │                               │  Fuzzy post-processing       │
└─────────────────────┘                               │  Language detection          │
                                                      └──────────────────────────────┘
```

---

## Prerequisites

| Dependency | Version | Notes |
|------------|---------|-------|
| Python | 3.9+ | tested on 3.11 and 3.12 |
| Tesseract OCR | 4.x or 5.x | system-level binary, not a pip package |
| Flutter SDK | 3.11.5+ | for the mobile client only |

### Installing Tesseract

`pytesseract` is just a Python wrapper — the actual binary must be installed separately.

| Platform | Install |
|----------|---------|
| Ubuntu / Debian | `sudo apt install tesseract-ocr` |
| macOS | `brew install tesseract` |
| Windows | Grab the installer from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), add to PATH |

Quick check:
```bash
tesseract --version
```

---

## Backend setup

From the repo root:

```bash
# create isolated environment
python -m venv backend/venv
source backend/venv/bin/activate   # Windows: backend\venv\Scripts\activate

# install all dependencies (pinned versions)
pip install -r backend/requirements.txt
```

**First-run note:** EasyOCR and PaddleOCR will download their model weights on first invocation (~200–400 MB each). This is automatic and only happens once — the models are cached locally after that. Make sure you have internet access for the first run.

Start the server:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Check it's alive:
```bash
curl http://localhost:8000/health
# → {"status":"ok"}
```

You'll need your machine's LAN IP for the mobile app:
```bash
ipconfig getifaddr en0   # macOS
hostname -I              # Linux
ipconfig                 # Windows (look for IPv4)
```

---

## Flutter app setup

```bash
cd flutter_app
flutter pub get
```

Edit `lib/config.dart` — put your machine's IP in there:

```dart
class BackendConfig {
  static String host = '192.168.0.200'; // ← your LAN IP here
  static int port = 8000;
  ...
}
```

Phone and laptop must be on the same Wi-Fi.

```bash
# Android (USB debugging enabled)
flutter run --release

# iOS (requires Xcode signing)
cd ios && pod install && cd ..
flutter run --release
```

For iOS you'll also need to open `ios/Runner.xcworkspace` in Xcode, set your signing team and a unique bundle ID under Signing & Capabilities.

---

## Reproducing the evaluation

This section documents the full reproducibility package for the accompanying IEEE paper.

All Python dependencies are pinned in `backend/requirements.txt` to ensure version-exact reproducibility. No GPU is required — all engines run on CPU.

### Dataset

| Location | Contents |
|----------|----------|
| `test_photos/` | 18 receipt images from the public [SROIE](https://rrc.cvc.uab.es/?ch=13) dataset + `blurry_failure_case.jpg` (intentionally degraded, used to test robustness under poor scan conditions) |
| `test_photos/ground_truth.json` | Reference transcriptions for every image |
| `manual_test_photos/` | Supplementary multilingual images (Chinese, German, Russian, handwritten, synthetic) for diversity testing |

### Dataset preparation

The dataset is already included in the repository. If you want to regenerate it from scratch (e.g. to verify provenance):

```bash
python prepare_dataset.py
```

This script downloads receipt images from public HuggingFace datasets (CORD-v2, FUNSD, and generated receipts), saves 18 samples as `sroie_*.jpg`, creates a blurred failure-case image, and writes `ground_truth.json`. No API keys are needed — HuggingFace datasets are publicly accessible.

### Running the benchmark

Make sure the backend is running first (see above), then:

```bash
python benchmark_eval.py
```

This evaluates all test images across three scenarios and writes results to `evaluation_results.csv`:

| Scenario | Engine | Post-processing | Language |
|----------|--------|-----------------|----------|
| Baseline | Tesseract | none | English |
| Optimized | EasyOCR | SymSpell fuzzy correction | English |
| Optimized | PaddleOCR | none | auto-detect |

A summary table is printed to stdout at the end.

### Output format

Each row in `evaluation_results.csv` contains:

| Column | Description |
|--------|-------------|
| `image` | filename |
| `scenario` | Baseline or Optimized |
| `engine` | tesseract, easyocr, or paddleocr |
| `fuzzy` | whether SymSpell post-processing was applied |
| `wer` | Word Error Rate (0–1) |
| `cer` | Character Error Rate (0–1) |
| `latency_s` | end-to-end request latency in seconds |
| `status` | ok, no_text_detected, timeout, etc. |
| `detected_language` | ISO 639-1 code from Lingua |

---

## Project layout

```
backend/
  main.py              API endpoints and request orchestration
  ocr_engine.py        EasyOCR / Tesseract / PaddleOCR wrappers
  preprocess.py        image preprocessing (deskew, binarisation)
  layout.py            text region detection (contour-based)
  fuzzy.py             SymSpell / pyspellchecker post-processing
  schemas.py           Pydantic request/response models
  requirements.txt     pinned Python dependencies
  symspell_dicts/      dictionary files for fuzzy correction

flutter_app/
  lib/config.dart      backend host/port — edit before running
  pubspec.yaml         Flutter dependencies

test_photos/           primary benchmark dataset (SROIE subset)
manual_test_photos/    supplementary multilingual test images
docs/                  IEEE paper source (.tex) and documentation

prepare_dataset.py     downloads and prepares the SROIE benchmark subset
benchmark_eval.py      runs the full evaluation pipeline
evaluation_results.csv latest benchmark output (committed for reference)
```

---

## API reference

A Postman collection covering all endpoints is included at `OCR_Backend.postman_collection.json`.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | liveness check |
| `/ocr` | POST | single-image OCR (base64 input) |
| `/ocr/batch` | POST | batch OCR for multiple images |
| `/evaluate` | POST | OCR + WER/CER metrics against reference text |
| `/evaluate/batch` | POST | batch evaluation with aggregate metrics |

### Example request

```bash
# single image OCR
curl -X POST http://localhost:8000/ocr \
  -H "Content-Type: application/json" \
  -d '{
    "image": "<base64-encoded JPEG or PNG>",
    "engine": "easyocr",
    "lang": "en",
    "fuzzy": true,
    "fuzzer": "symspell"
  }'
```

### Request parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `image` | string | required | base64-encoded JPEG or PNG (max 10 MB) |
| `engine` | string | `"easyocr"` | `easyocr`, `tesseract`, or `paddleocr` |
| `lang` | string | `"auto"` | ISO language code or `"auto"` for detection |
| `fuzzy` | bool | `false` | enable SymSpell/pyspellchecker post-processing |
| `fuzzer` | string | `"symspell"` | `"symspell"` or `"pyspellchecker"` |

---

## Privacy and ethical considerations

This system is designed with privacy as a core principle:

- All OCR processing happens on the local network. No image or text data is transmitted to external services.
- No user data is stored persistently — images are processed in memory and discarded.
- The system is a research prototype and should not be presented as a production-ready assistive tool. It has not been validated with end users in a clinical or accessibility study.
- The SROIE dataset used for evaluation is publicly available and contains no personal information.
