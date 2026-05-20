# Processing Pipeline Analysis

## Accepted input formats (actual)

- Backend accepts only **JPEG/PNG** base64 payloads (`backend/main.py::_decode_image`)
- Flutter picker allows `jpg/jpeg/png/pdf` (`flutter_app/lib/home_screen.dart::_pickFromFiles`)
- Therefore PDF support is **UI-exposed but backend-incompatible**.

## Pipeline stages

| Stage | Implemented? | Code evidence | Input | Output | Failure modes | Recommended tests |
|---|---|---|---|---|---|---|
| File acquisition (camera) | yes | `home_screen.dart::_captureFromCamera` | Camera image | Image bytes | Permission denied/camera unavailable | Permission-denied UI path; large photo handling |
| File acquisition (picker) | yes | `home_screen.dart::_pickFromFiles` | jpg/jpeg/png/pdf | File bytes | Invalid file, picker error | Pick each allowed extension; verify backend behavior |
| Transport to backend | yes | `ocr_service.dart::processBytes` POST JSON | image bytes + options | OCR JSON response | timeout/network/server errors | Offline backend, timeout, malformed endpoint |
| Request decode/validation | yes | `main.py::_decode_image` | base64 image | raw image bytes | invalid base64, >10MB, unsupported format | Negative tests for each validation branch |
| Preprocessing | yes | `preprocess.py::preprocess_image` | image bytes | preprocessed bytes + transform | decode errors, skew heuristics poor | Skewed/low-res docs before/after OCR comparison |
| Layout region detection | partially | `layout.py::detect_text_regions` | preprocessed image | bbox list | misses text, noisy contours | Dense docs, multi-column docs, receipts |
| OCR engine execution | yes | `ocr_engine.py::{run_easyocr,run_tesseract,run_paddleocr}` | image/regions + lang | (text, conf, bbox) tuples | engine unavailable, model/lang mismatch | Engine matrix test by language and document type |
| Reading-order reconstruction | partially | `layout.py::sort_reading_order` | bboxes | ordered bboxes | wrong order in complex layouts | Multi-column/page-like synthetic tests |
| Language detection | yes | `main.py::detect_language` | joined OCR text | ISO code / None | short/empty text, detection errors | Mixed-language and short-text cases |
| Optional fuzzy correction | yes | `fuzzy.py::apply_fuzzy_matching` | OCR text + lang + fuzzer | corrected text | wrong corrections; dictionary download failure | Offline mode + language fallback behavior |
| Response structuring | yes | `main.py::_process_image` + `schemas.py` | OCR tuples + transform | `OCRResponse` blocks/full_text | empty text becomes `no_text_detected` | Verify bbox mapping & status transitions |
| Evaluation metrics | yes | `main.py::_compute_metrics`, `/evaluate*` | expected + predicted text | WER/CER + error counts | expected text empty => metrics None | Unit checks for deterministic example pairs |
| Audio generation | yes (frontend) | `tts_service.dart`, `ocr_result_screen.dart` | OCR text | spoken audio | TTS language unavailable | Device with/without en-US voice |
| Output format | yes | `schemas.py` | internal blocks | JSON API + visual block list | N/A | Contract tests for fields and types |

## PDF/image handling summary

- **Image handling:** implemented (JPEG/PNG)
- **PDF parsing/rasterization:** not found in backend
- **Current closest flow for PDF:** app sends raw PDF bytes, backend rejects by magic-byte validation

## If no clear pipeline existed

Not applicable: a clear OCR pipeline exists in backend and UI, with specific endpoint/engine flow.
