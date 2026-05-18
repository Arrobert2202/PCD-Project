# Improvement Roadmap

## Immediate fixes

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Align README with current implementation state | Prevents overclaiming and confusion | `README.md` | Clear implemented/planned separation and accurate structure |
| Implement backend `/ocr` stub returning controlled schema (even before full OCR) | Unblocks integration testing | `backend/main.py` | Flutter can complete request/response flow with predictable output |
| Fix stale Flutter test scaffold (`MyApp` mismatch) | Restores basic test hygiene | `flutter_app/test/widget_test.dart`, `flutter_app/lib/main.dart` | Passing basic widget test in CI/local |

## 1-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Add minimal OCR backend using one engine (Tesseract or EasyOCR) | Establishes working end-to-end prototype | `backend/main.py`, new OCR helper module(s) | `/ocr` returns `full_text` and blocks from real images |
| Add backend API contract tests (`/health`, `/ocr`) | Prevent regressions | `backend/tests/*` | Automated pass/fail for API schema and error cases |
| Add visible transcript in UI | Supports low-vision and debugging | `flutter_app/lib/home_screen.dart` | On-screen text shown with spoken output |

## 3-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Add block-level navigation controls | Core accessibility objective | `flutter_app/lib/home_screen.dart`, `ocr_service.dart` | Users can move across blocks with announcements |
| Add evaluation starter package (`eval/`) with 20+ samples and ground truth | Enables quantitative reporting | `eval/*`, scripts, docs | Reproducible CER/WER outputs and dataset manifest |
| Add baseline pipeline and comparison script | Required academic rigor | `eval/*`, backend/client toggles | Side-by-side baseline vs proposed metrics table |

## 1-week improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Improve layout reconstruction for multi-block docs | Better navigability and understanding | backend OCR/layout modules | Improved reading-order metrics and user task outcomes |
| Add privacy and ethics UX elements (consent, warnings, retention policy) | Reduces harm/compliance risk | Flutter UI + docs + backend policies | Visible consent flow and documented privacy guarantees |
| Run structured usability study protocol | Supports accessibility claims | `eval/`, paper materials | Task metrics + qualitative findings |

## Optional extensions

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Add multilingual OCR/TTS support | Broader accessibility impact | backend OCR config + `tts_service.dart` + settings UI | Language switch options and multilingual results |
| Add PDF ingestion path | Better requirement coverage | backend ingestion modules + UI file picker | PDF test cases processed end-to-end |
| Confidence visualization and spoken uncertainty cues | Improves trust and safety | backend confidence outputs + UI/TTS messaging | Low-confidence regions clearly signaled |
