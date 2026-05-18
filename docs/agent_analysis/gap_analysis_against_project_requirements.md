# Gap Analysis Against Project 7 Requirements

| Requirement | Current evidence | Gap | Severity | Recommended action |
|---|---|---|---|---|
| OCR accuracy evaluation | `backend/requirements.txt` includes `jiwer`; README mentions CER/WER eval folder | No evaluation scripts, datasets, ground truth, or results found | critical | Add minimal evaluation harness with CER/WER script, fixed test set, and reproducible report output. |
| Layout extraction | Client model expects blocks (`flutter_app/lib/ocr_service.dart`) | No backend layout extraction code or block generation implementation | critical | Implement backend OCR endpoint returning block structure and reading order metadata. |
| Audio navigation or accessible navigation | TTS + semantic announcements exist (`home_screen.dart`, `tts_service.dart`) | No navigation by section/block/page; only monolithic readout | major | Add navigable unit controls (next/prev block, repeat current block) and announced context. |
| Privacy analysis for captured documents | README implies local setup; no formal privacy controls | No retention policy, no explicit consent text, no safe logging policy | major | Document and implement no-storage default, optional delete-after-process, and user-facing privacy notice. |
| Baseline comparison | No baseline code/results found | Missing simplest comparator and experiment protocol | critical | Define baseline (raw OCR text output), implement same-task comparison scripts, and report metrics consistently. |
| Test documents or dataset protocol | Not found in repository | No corpus definition, sampling protocol, annotation method | critical | Add small curated dataset manifest and annotation instructions to support academic reproducibility. |
| Evaluation report | Not found in repository | Missing metrics tables/plots and failure analysis | major | Generate evaluation artifacts (CSV/Markdown) plus error taxonomy examples. |
| IEEE-style paper/specification section | Not found (`.tex`, report docs not found) | Missing paper draft and integrated requirements-to-verification section | major | Create paper skeleton and requirement traceability table linked to implemented artifacts. |
| Reproducibility instructions | README provides basic run commands | Instructions do not match current implemented backend capabilities | major | Update README to current state; add exact commands for tests/evaluation and expected outputs. |
