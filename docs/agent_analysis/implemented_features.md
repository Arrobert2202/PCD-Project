# Implemented Features (Evidence-Based)

Status legend: `implemented` | `partially implemented` | `stub only` | `configured but unused` | `missing` | `unclear`

## Feature inventory

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Image input (JPEG/PNG) | implemented | `backend/main.py::_decode_image` accepts JPEG/PNG magic bytes | high | Enforced server-side; 10 MB cap |
| PDF input support | partially implemented | UI picker allows `pdf` (`flutter_app/lib/home_screen.dart`), backend rejects non-JPEG/PNG (`backend/main.py::_decode_image`) | high | UX mismatch; likely fails for selected PDFs |
| Camera capture | implemented | `ImagePicker().pickImage(source: ImageSource.camera)` in `home_screen.dart` | high | Permission behavior delegated to platform/plugins |
| File upload from device | implemented | `file_picker` in `home_screen.dart::_pickFromFiles` | high | Sends raw bytes to OCR endpoint |
| OCR via EasyOCR | implemented | `backend/ocr_engine.py::run_easyocr`; selected in `main.py::_run_engine` | high | Uses layout-detected crops |
| OCR via Tesseract | implemented | `backend/ocr_engine.py::run_tesseract`; engine selection in `main.py::_run_engine` | high | Runtime dependency on local Tesseract install |
| OCR via PaddleOCR | implemented | `backend/ocr_engine.py::run_paddleocr`; engine selection in `main.py::_run_engine` | high | Full-image OCR path |
| Language auto-detection | implemented | `backend/main.py::detect_language` with `lingua` | medium | Auto-detect applied after OCR text extraction |
| Layout detection (region proposals) | implemented | `backend/layout.py::detect_text_regions` | high | Used for EasyOCR path only |
| Reading-order reconstruction | partially implemented | `backend/layout.py::sort_reading_order` simple y/x grouping | medium | Heuristic, no complex document structures |
| Bounding box mapping back to original image | implemented | `PreprocessTransform.bbox_to_original` in `preprocess.py`, used in `main.py` | high | Supports deskew/upscale inverse mapping |
| Document understanding / summarization | missing | Not found in backend/flutter code | high | No summarization model or endpoint |
| Block classification (title/table/list/etc.) | missing | Not found | high | No semantic layout classes |
| TTS read-all output | implemented | `ocr_result_screen.dart::_toggleReadAll`, `tts_service.dart::speak` | high | Reads concatenated OCR output |
| TTS per-block output | implemented | `ocr_result_screen.dart::_readBlock` | high | Tap block to read selection |
| Navigable OCR blocks | implemented | block list with selected state; tap bbox overlays | high | Visual+audio block interaction |
| Screen-reader semantics labels | implemented | multiple `Semantics(...)` wrappers + `SemanticsService.announce` in `home_screen.dart` and `ocr_result_screen.dart` | high | Key controls labeled |
| Keyboard-first navigation | unclear | No explicit keyboard focus handling found | medium | Flutter defaults may help but not explicitly designed |
| ARIA/semantic HTML (web) | unclear | No dedicated accessible web UI code found | medium | Flutter web exists, but no web-specific accessibility audit code |
| OCR backend API | implemented | `/ocr`, `/ocr/batch`, `/evaluate`, `/evaluate/batch` in `backend/main.py` | high | Structured JSON responses via Pydantic |
| Health endpoint | implemented | `/health` in `backend/main.py` | high | Used by benchmark precheck |
| Batch OCR/evaluation | implemented | `BatchOCRRequest`, `BatchEvaluateRequest`; endpoints in `main.py` | high | Returns aggregate mean WER/CER in batch evaluate |
| OCR quality metrics (WER/CER) | implemented | `jiwer.process_words/process_characters` in `main.py::_compute_metrics` | high | Per-sample and aggregate |
| Benchmark automation script | implemented | `benchmark.py` | high | Downloads Kaggle datasets, evaluates engines |
| Baseline comparison capability (engine-to-engine) | implemented | `benchmark.py --engines ...` and comparison table | high | Baseline concept available via engine selection |
| Privacy safeguards: input size/type validation | implemented | `main.py::_decode_image` | high | Reduces malformed/oversized inputs |
| Privacy safeguards: transport security (TLS/auth) | missing | no auth, no HTTPS config in app/backend | high | LAN HTTP only |
| Privacy safeguards: retention/deletion policy | missing | not found in README/code docs | high | No explicit policy |
| Sensitive data persistence control | partially implemented | runtime debug image writes in `backend/preprocess.py::_dbg` and `dbg_boxes`; ignored by git in `.gitignore` | high | Debug outputs still persisted locally |
| Unit/integration tests (backend) | missing | no backend tests found | high | No pytest/unittest suite |
| Flutter tests | stub only | `flutter_app/test/widget_test.dart` references `MyApp` not present | high | Template test appears stale/broken |
| Reproducibility docs | partially implemented | README run steps + requirements/pubspec | medium | Missing full environment pinning and expected outputs |
