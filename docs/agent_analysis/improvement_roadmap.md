# Improvement Roadmap

## Immediate fixes

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Align UI input types with backend support (PDF mismatch) | Prevents avoidable user failure | `flutter_app/lib/home_screen.dart`, maybe README | PDF path disabled or fully supported with documented behavior |
| Add explicit privacy warning in app + README | Reduces misuse of sensitive docs | `flutter_app/lib/home_screen.dart`, `README.md` | Visible consent/warning text and updated docs |
| Stop logging raw OCR/ground-truth by default | Lowers leakage risk | `backend/main.py` | Logs no longer include full extracted text by default |

## 1-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Create normalized test manifest for `test_photos` | Stabilizes evaluation repeatability | `test_photos/*`, `benchmark_eval.py`, docs | Clean GT schema and reproducible parser |
| Add simple navigation controls (next/prev block) | Better non-visual navigation | `flutter_app/lib/ocr_result_screen.dart` | Demonstrable keyboard/button block traversal |
| Document baseline protocol and reporting template | Strengthens academic comparison | `docs/`, `benchmark_eval.py` | Fixed baseline configuration and result template |

## 3-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Add layout mini-benchmark (bbox + order checks) | Moves toward document-understanding evidence | new eval scripts/data + `backend/layout.py` | Quantitative layout metrics table |
| Add uncertainty communication (low confidence cues) | Prevents over-trust by users | `ocr_result_screen.dart`, `tts_service.dart` | UI/TTS indicates low-confidence blocks |
| Improve preprocessing ablation options | Can improve OCR quality systematically | `backend/preprocess.py`, benchmarking scripts | Comparative results showing best preprocessing setup |

## 1-week improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| End-to-end reproducibility package (preflight + env doc) | Enables reliable grading and collaboration | `README.md`, setup scripts, dependency docs | Fresh setup success checklist and smoke-test outputs |
| Accessibility-focused pilot protocol | Supports project theme claims | docs + optional instrumentation | Task completion/time/user feedback summary |
| IEEE paper scaffold with requirement traceability | Accelerates final paper quality | paper/docs artifacts | Draft with REQ mapping and figure/table placeholders |

## Optional extensions

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| True PDF pipeline (render pages + OCR + page navigation) | Broadens document coverage | frontend input handling + backend PDF stage | Working PDF demo and page-level navigation |
| Lightweight on-device OCR fallback | Improves privacy/offline robustness | Flutter side + model integration | Offline OCR path demo |
| Semantic block classification (header/item/total) | Better navigation and summaries | backend post-processing + UI | Structured output labels and targeted navigation |
