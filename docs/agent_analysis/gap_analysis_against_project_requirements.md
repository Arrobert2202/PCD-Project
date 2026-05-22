# Gap Analysis Against Project 7 Requirements

| Requirement | Current evidence | Gap | Severity | Recommended action |
|---|---|---|---|---|
| OCR accuracy evaluation | WER/CER endpoints and benchmark script (`backend/main.py`, `benchmark.py`) | No committed evaluation report/results in repo | major | Add reproducible evaluation report with fixed dataset subset and saved outputs |
| Layout extraction | Region detection + reading-order heuristics (`backend/layout.py`) | No advanced layout semantics (titles/tables/sections), only bbox grouping | major | Add block-type classification and structured export format |
| Audio navigation or accessible navigation | TTS read-all/read-block + semantics labels (`ocr_result_screen.dart`, `home_screen.dart`) | No robust non-visual task protocol; limited documented navigation patterns | major | Define and test navigation tasks for blind users; add focus-order and shortcut map |
| Privacy analysis for captured documents | Basic input validation and local processing orientation (`main.py`, README local Wi-Fi setup) | No explicit privacy policy, no retention/deletion controls; debug image persistence | critical | Add explicit privacy section + opt-out debug writing + deletion controls |
| Baseline comparison | Multi-engine comparisons possible via `benchmark.py --engines` | No formal baseline protocol and no baseline results committed | major | Define baseline condition and run comparable experiments with fixed settings |
| Test documents or dataset protocol | `test_photos/` examples and Kaggle-driven benchmark script | No curated, versioned evaluation set + ground truth in repo | major | Add small licensed benchmark subset + annotation protocol |
| Evaluation report | Runtime stats printing in benchmark | No structured report template/tables in docs | moderate | Add report template and generated summary artifacts |
| IEEE-style paper/specification section | Not found | Missing paper draft skeleton and requirement traceability table in repo | critical | Create IEEE scaffold and REQ-to-evidence matrix |
| Reproducibility instructions | README backend/flutter setup exists | Environment not fully pinned across platforms; missing expected outputs/troubleshooting | major | Add reproducibility checklist with versions, commands, and known failure modes |
