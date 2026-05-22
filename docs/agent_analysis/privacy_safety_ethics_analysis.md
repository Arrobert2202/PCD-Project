# Privacy, Safety, and Ethics Analysis

| Risk | Evidence | Impact | Mitigation | Implementation difficulty |
|---|---|---|---|---|
| OCR input images persisted as debug files | `backend/preprocess.py::_dbg` and `dbg_boxes` write images to `backend/debug/` | Sensitive document leakage on host machine | Gate debug writes behind `_DEBUG` flag and disable by default | low |
| No explicit data retention/deletion policy | Policy text not found in README/docs | User uncertainty and compliance risk | Add privacy section with storage/transit/retention statements | low |
| No auth/TLS for backend API | local HTTP in README and app config (`README.md`, `config.dart`) | LAN interception or unauthorized use on shared networks | Restrict to localhost or add token/TLS tunnel guidance | moderate |
| External dictionary download at runtime | `backend/fuzzy.py::_download_dict` fetches from GitHub | Network dependency and reproducibility/privacy concerns | Vendor/cache dictionaries in repo or package artifact | moderate |
| Potential false reassurance from OCR output | No confidence warnings in UI flow; confidence exists but not strongly surfaced for safety | Misreading critical content | Add confidence warnings and “verify manually” prompts | low |
| Inaccessible failure path for unsupported input | PDF allowed in picker but backend rejects non-image bytes | User frustration; inaccessible loop | Align accepted formats or add PDF preprocessing | moderate |
| No explicit consent/warning language | Not found in UI/readme | Ethical risk for sensitive docs and bystander capture | Add first-run consent and usage warning | low |
| Bias/performance uncertainty across languages/docs | Multi-language claims exist, but no published fairness/per-language eval report | Uneven performance for users across contexts | Report per-language/document-type metrics | moderate |
| Dataset licensing/usage ambiguity in benchmark workflow | `benchmark.py` pulls arbitrary Kaggle datasets | Legal/ethical uncertainty if dataset not vetted | Add approved dataset list + license checks | moderate |

## Additional notes

- Input validation exists (format and size checks in `main.py::_decode_image`) and is positive from a safety perspective.
- Local processing architecture (phone→local laptop backend) may reduce cloud exposure, but this is not documented as a formal privacy guarantee.
