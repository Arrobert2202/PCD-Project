# Reproducibility Audit

| Item | Status | Evidence | Problem | Recommended fix |
|---|---|---|---|---|
| README run instructions | partial | `README.md` includes backend + flutter run steps | Instructions imply OCR pipeline/eval artifacts not present | Update README to reflect actual implemented endpoints/features |
| Python dependency file | present | `backend/requirements.txt` | Includes OCR/eval deps not yet used in code | Keep, but mark planned vs currently used and add import-time tests |
| Flutter dependency file | present | `flutter_app/pubspec.yaml` | No committed lockfile (`pubspec.lock` ignored) | Commit lockfile for deterministic reproducibility |
| Environment variable strategy | missing | Host configured in code/settings (`config.dart`) | No `.env`/config profile for backend URL | Add environment-based config for dev/test/release |
| Sample data/dataset | missing | No `eval/`, `data/`, or dataset manifests found | Cannot reproduce evaluation claims | Add `eval/` package with sample set and annotation protocol |
| Evaluation scripts | missing | Not found in repository tree | CER/WER claims cannot be reproduced | Add scripts and expected-output examples |
| Automated backend tests | missing | No backend test files detected | API behavior not reproducibly verified | Add minimal pytest suite and instructions |
| Automated Flutter tests | partial/stale | `flutter_app/test/widget_test.dart` references `MyApp` | Test appears incompatible with current app class | Update test to current app and add smoke/integration tests |
| Build/test command verification in this environment | limited | `flutter` command unavailable; `pytest` unavailable | Tooling gaps prevent full verification in sandbox | Document required toolchain and validate in CI |
| Docker/Conda support | missing | No Dockerfile/compose/conda files found | Harder cross-platform reproducibility | Add optional containerized backend environment |
| Expected outputs/examples | missing | No API response examples in docs | Contract ambiguity for `/ocr` | Add canonical request/response samples in README/docs |
