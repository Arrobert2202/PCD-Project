# Processing Pipeline Analysis

## High-level finding
A concrete pipeline exists for **image OCR**; no robust end-to-end PDF parsing pipeline was found.

## Pipeline stages

| Stage | Implemented? | Code evidence | Input | Output | Failure modes | Recommended tests |
|---|---|---|---|---|---|---|
| Input acquisition (camera/file) | yes | `flutter_app/lib/home_screen.dart::_captureFromCamera`, `_pickFromFiles` | Camera capture or selected file | Raw file bytes | Camera permission denied; picker failure | Permission denial, canceled pick, corrupted file |
| Upload preprocessing on client | yes | `flutter_app/lib/ocr_service.dart::_prepareOcrUploadBytes` | Image bytes | Resized/re-encoded JPEG bytes | Decode failure fallback to original bytes | Very large image, EXIF rotation, tiny image |
| API payload build | yes | `ocr_service.dart::processBytes` | Upload bytes + options | JSON `{image, engine, lang, fuzzy, fuzzer}` | Network timeout, non-200 response | Offline backend, long request timeout path |
| Base64 decode + file validation | yes | `backend/main.py::_decode_image` | Base64 image string | Validated byte buffer | Invalid base64, >10MB, non-JPEG/PNG | Invalid base64, PNG/JPEG boundary, unsupported format |
| Backend preprocessing | yes | `backend/preprocess.py::preprocess_image` | Image bytes | JPEG bytes + transform metadata | Decode/encode errors, deskew outlier | Extreme skew, low contrast, noisy scans |
| Text region detection | partially (engine-specific) | `backend/layout.py::detect_text_regions` called for EasyOCR only in `_run_engine` | Preprocessed image | List of bboxes | No contours => empty list | Dense receipts, multi-column docs, low-res text |
| OCR engine execution | yes | `run_easyocr`/`run_tesseract`/`run_paddleocr` in `backend/ocr_engine.py` | Preprocessed image (+bboxes for EasyOCR) | Raw tuples `(text, confidence, bbox)` | Missing models/runtime, engine errors | Per-engine smoke tests and multilingual samples |
| Reading-order reconstruction | yes (layout path) | `sort_reading_order` in `backend/layout.py` | Bboxes | Ordered bboxes | Wrong line grouping on complex layouts | Two-column documents, tables, mixed font sizes |
| Bounding-box remap to original image | yes | `PreprocessTransform.bbox_to_original` in `backend/preprocess.py` | OCR bbox in transformed space | Bbox in original space | Geometric drift after deskew/scale | Pixel-level overlay check on known samples |
| Block assembly/full text | yes | `backend/main.py::_process_image` | Raw OCR tuples | `TextBlock[]`, `full_text` | Empty blocks -> `no_text_detected` | Empty text lines, null confidences |
| Language assignment | partially | `backend/main.py::detect_language` | Concatenated OCR text | ISO code or `None` | Mis-detection on short/noisy text | Short text strings, mixed-language docs |
| Fuzzy correction | optional implemented | `backend/fuzzy.py::apply_fuzzy_matching` | OCR block text | Corrected text lines | Wrong corrections, dict download failure | Domain terms, non-Latin scripts, offline mode |
| Accessibility rendering + TTS | yes | `ocr_result_screen.dart`, `tts_service.dart` | OCR response | Visual block UI + spoken text | TTS unavailable, no language adaptation | Read-all interruption, per-block tap flow |
| Evaluation metrics | yes | `/evaluate*` in `backend/main.py`; `benchmark*.py` scripts | OCR output + expected text | WER/CER + error counts | GT mismatch/format issues | Controlled known GT samples |

## Accepted input formats (implemented now)
- **Backend accepts:** JPEG, PNG only (`backend/main.py::_decode_image` magic checks)
- **UI selectable:** jpg/jpeg/png/pdf (`home_screen.dart`)
- **Mismatch:** PDF selectable in UI but backend path is image-only (likely runtime error)

## Closest available flow for unsupported stages
- **PDF parsing/layout extraction for digital PDFs:** not found.
- Closest flow is image-based OCR with contour-based regioning (EasyOCR path) and line-level grouping (Tesseract/PaddleOCR paths).
