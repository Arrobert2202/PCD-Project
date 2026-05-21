# Gap Analysis Against Project 7 Requirements

| Requirement | Current evidence | Gap | Severity | Recommended action |
|---|---|---|---|---|
| OCR accuracy evaluation | `/evaluate` and `/evaluate/batch` compute WER/CER (`backend/main.py`); scripts `benchmark.py`, `benchmark_eval.py`; `evaluation_results.csv` exists | No standardized protocol (fixed splits, confidence intervals, statistical reporting) | major | Freeze dataset split/version, add repeatable experiment script + summary report generation |
| Layout extraction | Bounding boxes + reading order (`backend/layout.py`, `backend/preprocess.py`, `ocr_result_screen.dart`) | No explicit layout classes (title/table/paragraph), no structural hierarchy | major | Add minimal block taxonomy and reading-order validation set |
| Audio navigation / accessible navigation | TTS full text + block tap reading; Semantics labels and announcements (`home_screen.dart`, `ocr_result_screen.dart`, `tts_service.dart`) | No advanced navigable model (section/page landmarks, skip controls, uncertainty narration) | major | Add navigation modes (next/prev block, confidence warning, heading-like grouping) |
| Privacy analysis for captured docs | 10MB + JPEG/PNG validation (`_decode_image` in `backend/main.py`) | No explicit privacy statement, no retention policy, logs store OCR and expected text (`backend/logs/backend.log`) | critical | Add privacy notice, configurable log redaction, retention/deletion controls |
| Baseline comparison | `benchmark_eval.py` defines baseline (`tesseract`) and optimized conditions | Baseline rationale and fairness controls not documented | moderate | Document baseline justification, fix scenario naming, enforce comparable preprocessing |
| Test documents / dataset protocol | `test_photos/`, `ground_truth.json`, `prepare_dataset.py`, Kaggle/HF loaders | Ground-truth format is irregular; provenance/versioning not formalized | major | Normalize GT schema + add dataset manifest (source, split, license, checksum) |
| Evaluation report | CSV output exists (`evaluation_results.csv`) | No auto-generated narrative report, no error taxonomy breakdown | major | Generate markdown/CSV report with aggregate + failure-case analysis |
| IEEE-style paper + integrated spec section | Not found in repository | Missing manuscript skeleton, requirements traceability | critical | Add paper draft structure and requirement-to-evidence table |
| Reproducibility instructions | Basic run steps in `README.md` | Missing full environment pinning and working CI-like command set; `flutter` and `pytest` unavailable in this environment | major | Add environment prerequisites, version matrix, smoke-test script |

## Severity key
- **critical:** blocks project objectives or research validity
- **major:** substantial quality/reliability gap
- **moderate:** notable but tractable weakness
- **minor:** polish/documentation-level issue
