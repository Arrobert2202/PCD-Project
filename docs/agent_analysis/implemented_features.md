# Implemented Features (Evidence-Based)

Status scale used: `implemented`, `partially implemented`, `stub only`, `configured but unused`, `missing`, `unclear`.

## Document input support

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Camera image capture on mobile | implemented | `flutter_app/lib/home_screen.dart::_capture` uses `ImagePicker().pickImage(source: ImageSource.camera)` | high | Core input path is live in UI flow. |
| Selecting existing photo/document file | missing | No `ImageSource.gallery` use in app code | high | iOS plist includes photo library description but code path not found. |
| PDF file input | missing | No PDF dependency/use in Flutter or backend source | high | README does not provide implemented PDF flow. |

## OCR/text extraction

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| OCR API contract expected by client | partially implemented | `flutter_app/lib/ocr_service.dart` expects `/ocr` JSON response with blocks/full_text | high | Client side exists. |
| Backend OCR endpoint (`POST /ocr`) | missing | `backend/main.py` only defines `/health` | high | Client currently points to nonexistent route. |
| EasyOCR/Tesseract integration | configured but unused | Packages in `backend/requirements.txt`; no imports/calls in `backend/main.py` | high | Dependency declaration without implementation. |

## Layout analysis

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Block-level layout output consumption in app | partially implemented | `OcrResponse.blocks` model in `flutter_app/lib/ocr_service.dart` | medium | App receives blocks but does not expose navigation UI for blocks. |
| Layout extraction logic in backend | missing | No layout/box code in backend source | high | README claim not supported by current code. |

## Summarization/document understanding

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Summarization or semantic understanding | missing | No NLP/summarization modules or calls found | high | Only full-text readout pathway exists on client side. |

## Audio output

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Text-to-speech playback | implemented | `flutter_app/lib/tts_service.dart::speak`, `home_screen.dart::_tts.speak(_text)` | high | Reads extracted text aloud. |
| Stop playback control | implemented | `home_screen.dart::_stop()` and Stop button in playing state | high | User can interrupt speech. |
| Multi-language voice config | missing | `tts_service.dart` sets only `en-US` | high | No locale switching UI/config. |

## Navigation/accessibility

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Basic semantics labels on key widgets | implemented | `Semantics(...)` wrappers in `home_screen.dart` | high | Labels for settings, scan, stop, inputs, status. |
| Screen-reader announcements for state changes | implemented | `SemanticsService.announce` in `_announce` | high | Announces progress/errors/completion. |
| Keyboard-first navigation model | unclear | Flutter widgets present; explicit focus traversal not found | medium | Likely mobile touch-first UX. |
| Structured navigation by page/section/block | missing | No UI for block traversal despite `blocks` model | high | Accessibility gap for document navigation. |

## UI

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Mobile UI with scan workflow | implemented | `home_screen.dart` scaffold/status/main button/settings dialog | high | End-to-end user interaction scaffold exists. |
| Backend host/port settings at runtime | implemented | `_showSettings` updates `BackendConfig.host/port` | high | Helps local-network setup. |
| OCR result text display on screen | missing | `_text` assigned but not rendered in widgets | high | Text is spoken, not visibly shown. |

## Backend/API

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Health endpoint | implemented | `backend/main.py:@app.get('/health')` | high | Minimal backend availability check. |
| OCR processing API | missing | no `/ocr` route in backend source | high | Blocks complete mobile flow. |

## Evaluation

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Declared intent to evaluate CER/WER | configured but unused | `README.md` mentions `eval/`; `backend/requirements.txt` includes `jiwer` | medium | No `eval/` directory or scripts found. |
| Baseline comparison implementation | missing | No baseline scripts/results found | high | Needed for project requirement. |

## Privacy/security

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Local-network architecture intent | partially implemented | README states laptop + same Wi-Fi; `config.dart` local host/port | medium | No technical enforcement of local-only traffic. |
| Consent/privacy notice in app | missing | No privacy or consent UI text in app code | high | Sensitive document handling not communicated. |
| Data retention/deletion policy | missing | No backend storage/deletion code beyond current minimal backend | high | Must be specified for accessibility use case. |

## Testing

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Flutter widget test file exists | stub only | `flutter_app/test/widget_test.dart` default counter test | high | References `MyApp` (not present), so stale template. |
| Backend tests | missing | No backend test files found | high | No API contract verification. |

## Reproducibility

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Setup instructions in README | partially implemented | README has backend + flutter commands | high | Instructions refer to missing OCR/eval components. |
| Version-pinned dependencies | partially implemented | Python deps pinned; Flutter deps semver ranges | high | No lockfiles committed for deterministic installs. |
