# Privacy, Safety, and Ethics Analysis

| Risk | Evidence | Impact | Mitigation | Implementation difficulty |
|---|---|---|---|---|
| OCR content logged to disk | `backend/main.py` logs `[OCR full text]`; `backend/logs/backend.log` includes text samples/ground truth | Sensitive document data leakage on host | Add redaction toggle, default no raw text logging, structured minimal logs | medium |
| Ground-truth text logging during evaluation | `backend/main.py` logs `[Ground truth]` in evaluate endpoints | Exposure of labeled/private datasets | Log only hash/ID, not content; gated debug mode | low |
| No documented retention/deletion policy | No policy found in README/docs | Users cannot assess privacy lifecycle | Add policy section: storage location, retention time, deletion command | low |
| Runtime external downloads for dictionaries | `backend/fuzzy.py` downloads from GitHub raw URLs | Network metadata leak; supply-chain stability risk | Vendor/freeze dictionaries or checksum-validate download | medium |
| Local-network unencrypted transport | `BackendConfig.ocrEndpoint` uses `http://` | OCR payload interception on insecure LAN | Prefer localhost/USB tunneling for demos, document secure network assumptions | medium |
| No explicit user consent/warning UI | No consent text found in Flutter screens | Users may upload sensitive docs without warning | Add first-run consent + “do not scan sensitive docs on shared network” warning | low |
| Over-trust risk from OCR errors | Evaluation CSV/logs show frequent high WER/CER and no-text cases | Incorrect information may be acted upon | Display confidence and uncertainty messages; encourage manual verification | medium |
| Accessibility bias across languages | TTS hardcoded `en-US`; OCR language support uneven by engine | Unequal experience for non-English users | Auto-select TTS language + language-specific fallback message | medium |
| Potential stale host configuration | Backend IP manually editable (`config.dart`, settings dialog) | Misrouting to wrong host, accidental data exposure | Validate/confirm host before sending first request | low |
| False reassurance in docs/comments | Postman description mentions preprocessing steps not observed in code | Mismatch between claims and behavior | Align docs with implemented pipeline; mark planned vs implemented | low |

## Additional notes
- Processing appears intended for local backend execution, which is better than mandatory cloud OCR, but privacy guarantees are currently implicit rather than explicit.
- Ethical framing for visually impaired users should include uncertainty communication and autonomy (user-controlled playback/navigation).
