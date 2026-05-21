# IEEE Paper Readiness Assessment

## Possible paper title (based on actual repo)
**ReadDoc: A Mobile-to-Local OCR Pipeline with Block-Level Audio Navigation for Accessible Document Reading**

## Abstract skeleton
1. **Problem:** Visually impaired users need accessible document reading from camera captures.
2. **Approach:** Flutter mobile client + FastAPI OCR backend with multi-engine OCR and optional fuzzy correction.
3. **System details:** Region detection, reading-order sorting, block overlays, TTS playback.
4. **Evaluation:** WER/CER and latency via backend evaluation endpoints and benchmark scripts.
5. **Findings/limits:** Current strengths and failure modes (blur, no-text cases, privacy/reproducibility gaps).

## Keywords
Accessible OCR; assistive technology; document understanding; text-to-speech; FastAPI; Flutter; WER/CER

## Likely contribution statement (supported by current code)
- Practical local-network architecture for phone capture + OCR backend.
- Multi-engine OCR comparison pipeline with WER/CER evaluation endpoints.
- UI that links OCR blocks to tappable overlay and spoken output.

## Missing evidence before strong IEEE claims
- Formal user study for visually impaired participants (not found)
- Standardized reproducible benchmark protocol with pinned dataset version
- Privacy policy and threat model
- Layout understanding metrics beyond OCR text accuracy

## Required figures
1. System architecture diagram (client/backend/engines)
2. Processing pipeline diagram (decode → preprocess → OCR → output)
3. UI screenshots (capture screen + overlay/readout screen)
4. Failure-case examples (blurred, complex layout)

## Required tables
1. Engine comparison (WER/CER/latency/no-text)
2. Ablation (fuzzy on/off, lang modes)
3. Risk/limitations and mitigations
4. Requirement traceability (integrated specification)

## Integrated specification section draft

| ID | Requirement | Priority | Verification method | Current evidence | Missing evidence |
|---|---|---|---|---|---|
| REQ-01 | System shall extract text from camera-captured documents | high | `/ocr` endpoint test with sample set | `backend/main.py`, `flutter_app/lib/ocr_service.dart` | Formal acceptance criteria document |
| REQ-02 | System shall provide navigable text blocks for interaction | high | Verify bbox blocks + UI selection flow | `backend/schemas.py::TextBlock`, `ocr_result_screen.dart::_readBlock` | Quantitative navigation usability results |
| REQ-03 | System shall provide audio output of recognized text | high | TTS functional test (read-all + block read) | `tts_service.dart`, `ocr_result_screen.dart` | Multi-language TTS validation |
| REQ-04 | System shall evaluate OCR quality against baseline | high | Run `benchmark_eval.py` and compare scenarios | `benchmark_eval.py`, `evaluation_results.csv` | Pinned dataset protocol + statistical significance |
| REQ-05 | System shall handle document privacy responsibly | high | Audit logs/storage/consent workflow | Input checks + local backend in code | Explicit privacy policy, log redaction, retention policy |
| REQ-06 | System shall support reproducible execution | medium | Fresh-environment runbook validation | README setup exists | Environment lock, CI/smoke script, dependency verification |
| REQ-07 | System shall support structured layout extraction | medium | Bbox + reading-order tests | `layout.py`, bbox output in API | Layout classification/semantic structure metrics |
| REQ-08 | System shall include clear limitations and uncertainty cues | medium | UI/UX inspection + user tests | Partial confidence display in result UI | Spoken uncertainty warnings, user-study evidence |

## Limitations and threats to validity
- Dataset/ground truth formatting may bias metric computation.
- OCR engine environment differences (GPU, language packs) can materially change results.
- Accessibility claims are currently feature-based, not user-study validated.
- Privacy claims cannot be strong without explicit governance artifacts.
