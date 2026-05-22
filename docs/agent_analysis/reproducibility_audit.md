# Reproducibility Audit

| Item | Status | Evidence | Problem | Recommended fix |
|---|---|---|---|---|
| Backend run instructions | present | `README.md` backend section | No automated setup script | Add one-command setup script or Make target |
| Flutter run instructions | present | `README.md` Flutter section | Device/toolchain assumptions not fully specified | Add tested Flutter SDK/version and platform notes |
| Backend dependencies file | present | `backend/requirements.txt` | Heavy platform-specific dependencies may fail | Add tested OS matrix and troubleshooting |
| Flutter dependencies file | present | `flutter_app/pubspec.yaml` | `pubspec.lock` ignored; exact transitive versions vary | Commit lockfile or document reproducible strategy |
| Environment variables | partial | benchmark Kaggle credentials in `benchmark.py` docstring | No centralized env var documentation | Add `.env.example` and env section in README |
| Sample data | partial | `test_photos/` exists | No paired ground-truth labels in repo | Add small labeled sample set |
| Evaluation scripts | present | `benchmark.py`, `/evaluate*` endpoints | No committed baseline outputs | Add `eval/results` artifacts or reproducible generation target |
| Test commands | partial | `flutter analyze` mention in analysis options comments; Flutter test exists | test file stale (`MyApp` mismatch), backend tests absent | Fix Flutter test and add backend unit/integration tests |
| Docker/Conda support | not found | no Dockerfile/conda files found | Harder setup portability | Add Dockerfile (backend) and optional compose |
| Fixed versions | partial | most backend deps pinned; Flutter deps semver ranges | Full determinism not guaranteed | tighten pins for benchmark runs |
| Expected outputs documented | partial | API schemas and benchmark printouts infer outputs | no official expected-result examples | add sample request/response and benchmark output snapshot |
