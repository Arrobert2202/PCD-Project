# Improvement Roadmap (Realistic)

## Immediate fixes

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Align file input support with backend (remove PDF option or add explicit block) | Prevents broken accessible flow | `flutter_app/lib/home_screen.dart` | Upload behavior matches backend constraints |
| Disable debug image persistence by default | Reduces privacy leakage risk | `backend/preprocess.py`, README | No new debug files during normal OCR runs |
| Fix stale Flutter test template | Restores basic CI/test signal | `flutter_app/test/widget_test.dart` | `flutter test` passes in configured environment |

## 1-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Add explicit privacy and limitations section in README | Required for ethical and paper clarity | `README.md` | Clear documented data handling and caveats |
| Add benchmark usage doc with fixed command examples | Improves reproducibility | `README.md`, `docs/` | Repeatable evaluation instructions |
| Add API examples with expected response schema | Improves integration reliability | `README.md` or `docs/api.md` | Contract examples for `/ocr` and `/evaluate` |

## 3-day improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Implement PDF rasterization before OCR | Closes major feature gap | backend input pipeline + Flutter upload flow | Successful OCR from PDF pages |
| Add confidence-aware user warnings | Safer assistive output | `flutter_app/lib/ocr_result_screen.dart` | UI and speech warnings on low-confidence blocks |
| Add small in-repo annotated evaluation subset | Enables reproducible experiments | new eval data folder + scripts | Deterministic benchmark results committed |

## 1-week improvements

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| Strengthen layout understanding (block grouping/classification) | Better navigation and doc usefulness | `backend/layout.py`, response schemas | Structured block types and better order metrics |
| Add accessibility task evaluation protocol | Needed for project requirement evidence | `docs/`, optional app telemetry | Task success/time/error report |
| Produce IEEE-ready result tables and figures | Accelerates final paper | `docs/`, benchmark outputs | Draft paper-ready tables/plots |

## Optional extensions

| Task | Why it matters | Files likely affected | Expected evidence after completion |
|---|---|---|---|
| On-device OCR fallback mode | Reduces network/privacy risks | Flutter app + optional local model integration | Offline processing demo |
| User profile for speech preferences and language | Improves accessibility personalization | Flutter settings/state | Configurable TTS behavior persisted |
| Document structure audio summaries | Better high-level navigation | backend understanding module + UI | Section-level navigation commands |
