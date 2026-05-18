# Processing Pipeline Analysis

## Current state summary
The repository contains a **client-side intended pipeline** (capture → upload → parse response → TTS), but the **server-side OCR pipeline is not implemented** in current backend code.

## Pipeline stages

| Stage | Implemented? | Code evidence | Input | Output | Failure modes | Recommended tests |
|---|---|---|---|---|---|---|
| Document acquisition (camera) | Yes | `home_screen.dart::_capture` with `ImageSource.camera` | Live camera frame/photo | Local image file path | Camera permission denied, user cancels | Device test: deny permission, cancel capture, success capture. |
| Input format acceptance | Partial | Camera path implies image files; no PDF path | Mobile image file | Multipart upload file | Non-image input path not exposed | Add unit/integration test for unsupported MIME handling once backend exists. |
| Upload to backend | Yes (client side) | `ocr_service.dart::MultipartRequest('POST', /ocr)` | File bytes | HTTP response stream | Timeout (15s), network errors, non-200 | Mock server tests for timeout, 500, malformed JSON. |
| OCR engine execution | No (server side) | No OCR code in `backend/main.py` | Would be uploaded image | Would be extracted text/blocks | 404 endpoint or unimplemented behavior | Add backend tests for OCR endpoint contract and engine fallback behavior. |
| Preprocessing (denoise/threshold/deskew) | No | Not found in backend code | Raw image | Preprocessed image | N/A | Add deterministic preprocessing unit tests with fixture images. |
| Text extraction | No (backend), expected by client | Client expects `full_text` in JSON | Image | `full_text` string | Missing key, empty text | Contract tests asserting presence/format of `full_text`. |
| Layout/bounding boxes | No (backend), expected schema exists | Client model `OcrBlock(index,text,confidence)` | OCR output | Block list | Missing/invalid `blocks` list | Contract tests for block order/index/confidence ranges. |
| Reading-order reconstruction | No | No ordering logic found | OCR detections | Ordered blocks | Incorrect order harms accessibility | Add reading-order acceptance tests with multi-column samples. |
| Block classification (title/paragraph/table) | No | Not found | Text/layout blocks | Labeled blocks | N/A | Add schema + classifier tests only if feature added. |
| Summary/document understanding | No | Not found | Extracted text | Summary/structured understanding | N/A | Add baseline summarization evaluation only after implementation. |
| Audio generation (TTS) | Yes | `tts_service.dart` + `_tts.speak(_text)` | `full_text` | Speech playback | TTS unavailable/language unsupported | Device tests for TTS unavailable and completion callback behavior. |
| Output format to user | Partial | Spoken output + status card; no text pane | OCR response | Audio + status messages | User cannot navigate long docs | Add UI tests for block navigation and repeat controls. |

## Closest implemented flow (inferred from code)
1. User taps scan.
2. App captures an image.
3. App uploads image to `http://<host>:<port>/ocr`.
4. If valid JSON returns, app reads `full_text` aloud.
5. Otherwise app enters error state and announces error.

Because step 4 depends on a currently missing backend endpoint, end-to-end OCR/document understanding is not verifiable in current checkout.
