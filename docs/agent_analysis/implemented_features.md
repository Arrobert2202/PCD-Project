# Implemented Features (Evidence-Based)

Status legend: `implemented` | `partially implemented` | `stub only` | `configured but unused` | `missing` | `unclear`

| Feature | Status | Evidence in repository | Confidence | Notes |
|---|---|---|---|---|
| Camera image capture | implemented | `flutter_app/lib/home_screen.dart` (`_captureFromCamera`) | high | Uses `image_picker` camera source |
| Local file input (jpg/jpeg/png) | implemented | `home_screen.dart` (`allowedExtensions`) + `ocr_service.dart` image processing | high | End-to-end image path works |
| Local file input (pdf) | partially implemented | `home_screen.dart` allows `pdf`; backend `_decode_image` only accepts JPEG/PNG in `backend/main.py` | high | PDF likely fails at decode/format check |
| OCR via EasyOCR | implemented | `backend/ocr_engine.py::run_easyocr`; selected in `_run_engine` (`backend/main.py`) | high | Uses region-based OCR on detected boxes |
| OCR via Tesseract | implemented | `backend/ocr_engine.py::run_tesseract`; engine route in `_run_engine` | high | Requires system Tesseract install |
| OCR via PaddleOCR | implemented | `backend/ocr_engine.py::run_paddleocr`; engine route in `_run_engine` | high | Full-image OCR path |
| OCR language auto-detection | partially implemented | `backend/main.py::detect_language` with `lingua` after OCR | medium | OCR itself uses `en` when `lang=auto`; detection is post-hoc metadata |
| Layout region detection | implemented | `backend/layout.py::detect_text_regions` | high | Adaptive threshold + dilation + contour filtering |
| Reading order reconstruction | implemented | `backend/layout.py::sort_reading_order` | high | Line grouping by y-centers |
| Bounding box output in API | implemented | `backend/schemas.py::BoundingBox`; mapped in `_process_image` | high | Returned per `TextBlock` |
| Coordinate remapping after preprocess | implemented | `backend/preprocess.py::PreprocessTransform.bbox_to_original` | high | Undo deskew + scale |
| Image preprocess (scale + deskew) | implemented | `backend/preprocess.py::preprocess_image` | high | No explicit CLAHE/denoise in current code |
| Fuzzy post-correction (SymSpell/PySpellchecker) | implemented | `backend/fuzzy.py::apply_fuzzy_matching`; toggles from UI | high | Language fallback behavior implemented |
| Document understanding (semantic fields/sections) | missing | Not found in backend response models or pipeline | high | Output is plain blocks + full_text |
| Summarization | missing | Not found in code paths or dependencies | high | No summarizer model/service |
| Audio output (TTS) | implemented | `flutter_app/lib/tts_service.dart`; invoked in `ocr_result_screen.dart` | high | Reads full text and individual blocks |
| Audio navigation by text block | implemented | `ocr_result_screen.dart::_readBlock` + tap targets over bboxes | high | Supports granular per-block reading |
| Screen-reader announcements for state changes | implemented | `home_screen.dart::_announce` using `SemanticsService.announce` | high | Announces processing/errors |
| Semantic labels for controls | implemented | Multiple `Semantics(...)` wrappers in `home_screen.dart`, `ocr_result_screen.dart` | high | Present for key controls |
| Keyboard-only navigation pattern | unclear | Flutter defaults exist; no explicit focus traversal logic found | low | Needs runtime verification on desktop/web targets |
| Backend API (health + OCR + evaluation) | implemented | `backend/main.py` endpoints | high | Includes batch variants |
| Evaluation metrics WER/CER in API | implemented | `_compute_metrics` + `/evaluate` responses (`backend/main.py`) | high | Uses jiwer word/char metrics |
| Baseline-vs-optimized evaluation scripting | implemented | `benchmark_eval.py::SCENARIOS` (`Baseline` vs `Optimized`) | high | Scenario naming partly duplicated |
| Benchmark automation over Kaggle dataset | implemented | `benchmark.py` | high | Includes ground-truth layout heuristics |
| Saved evaluation artifact | implemented | `/evaluation_results.csv` committed | high | Contains per-image metrics |
| Privacy policy/consent workflow in UI | missing | Not found in Flutter screens | high | No user-facing consent text |
| Data retention/deletion policy | missing | Not found in docs/config/code | high | Logs may persist OCR/ground truth text |
| Sensitive logging controls | partially implemented | Rotating logger in `backend/main.py`; logs OCR full text and ground truth | high | Rotation exists, content minimization absent |
| Unit/integration tests (backend OCR logic) | missing | No backend tests found | high | `pytest` not configured in environment |
| UI tests aligned to current app | missing | `flutter_app/test/widget_test.dart` references `MyApp` counter template | high | Does not match current `App` structure |
| Reproducibility scripts (dataset prep + eval) | implemented | `prepare_dataset.py`, `benchmark.py`, `benchmark_eval.py` | high | Useful but env setup incomplete |
| Containerized/declarative environment setup | missing | No Dockerfile/compose/conda/lockfiles found | high | Reproducibility risk |

## Notes on uncertain/indirect evidence
- `docs/languages.md` includes machine-specific paths and install claims; treat as **inferred/environment-specific**, not portable guarantees.
- Postman description claims contrast enhancement and denoising, but current `preprocess.py` does not clearly implement these steps.
