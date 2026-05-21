# Reproducibility Audit

| Item | Status | Evidence | Problem | Recommended fix |
|---|---|---|---|---|
| Backend run instructions | partially available | `README.md` backend section | No full OS/package preflight (Tesseract, CUDA/GPU expectations) | Add prerequisites matrix and preflight script |
| Flutter run instructions | partially available | `README.md` flutter section | Environment assumptions not explicit (Flutter SDK version/toolchain) | Add pinned Flutter version and setup verification steps |
| Backend dependencies file | available | `backend/requirements.txt` | Heavy deps may fail on unsupported hardware/OS | Add optional dependency groups and compatibility notes |
| Frontend dependencies file | available | `flutter_app/pubspec.yaml` | No lockfile committed (`pubspec.lock` ignored) | Consider lockfile or documented exact package resolution strategy |
| Environment variables documentation | partial | `backend/preprocess.py` uses `OCR_*` env vars | Not documented in README | Document all tunable env vars and defaults |
| Sample data availability | available | `test_photos/*`, `ground_truth.json`, `manual_test_photos/*` | Ground truth format is hard to parse consistently | Provide normalized GT JSON schema + converter |
| Evaluation scripts | available | `benchmark.py`, `benchmark_eval.py`, `prepare_dataset.py` | Multiple flows, no single canonical pipeline | Add one canonical `run_evaluation.sh`/documented sequence |
| Expected outputs documented | partial | `evaluation_results.csv` present | No expected metric ranges or success criteria | Add benchmark acceptance criteria section |
| Automated tests (backend) | missing | no backend test files found | Cannot validate core logic quickly | Add minimal API/unit smoke tests |
| Automated tests (frontend) | broken/stale | `flutter_app/test/widget_test.dart` uses `MyApp` counter template | Test does not match current app | Replace with tests targeting `App` and OCR flow widgets |
| Lint/build command reproducibility | failing in this environment | `python3 -m pytest` missing module; `flutter` command missing | Tooling not provisioned here; commands not self-validating | Add setup checks and documented dependency installation |
| Container/isolated env support | missing | no Docker/Conda files found | Hard to reproduce across machines | Add Dockerfile or devcontainer for backend at minimum |
