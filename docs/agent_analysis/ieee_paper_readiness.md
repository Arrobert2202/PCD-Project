# IEEE Paper Readiness Assessment

## Possible title (based on current repo)
**“ReadDoc: A Mobile Camera-to-Speech Frontend for Accessible Document Reading with Planned OCR Backend Integration”**

## Abstract skeleton
1. Problem context: accessible document reading for visually impaired users.
2. System scope in current prototype: mobile capture, backend request contract, TTS output.
3. Current implementation boundary: backend OCR route not yet implemented in this checkout.
4. Planned evaluation: OCR quality + accessibility task metrics vs baseline.
5. Contributions and limitations.

## Keywords
- accessible OCR
- document understanding
- Flutter mobile accessibility
- text-to-speech
- visually impaired interaction
- evaluation methodology

## Likely contribution statement (current evidence)
- A mobile accessibility-oriented UI scaffold integrating camera capture, OCR API client contract, and speech output.
- Preliminary accessibility instrumentation via semantic labels and spoken state announcements.
- Clear gap identification for OCR backend, layout understanding, and evaluation pipeline.

## Missing evidence blocking a strong paper
- Implemented OCR backend and layout extraction.
- Quantitative OCR and usability results.
- Baseline comparison results.
- Dataset and reproducibility package.
- Ethics/privacy implementation and protocol section.

## Required figures
1. Architecture diagram (frontend/backend + data flow).
2. Processing pipeline diagram (current vs target).
3. UI screenshots for scan/read/error states.
4. Evaluation workflow diagram (dataset → metrics → comparison).

## Required tables
1. Requirement traceability table (specification section).
2. OCR metrics table (CER/WER).
3. Task-level usability outcomes.
4. Ablation/baseline comparison table.

## Integrated specification section draft

| ID | Requirement | Priority | Verification method | Current evidence | Missing evidence |
|---|---|---|---|---|---|
| REQ-01 | System shall capture document images from mobile camera | high | Functional test on device | `home_screen.dart::_capture` | Cross-device reliability results |
| REQ-02 | System shall extract text from captured image via backend OCR | high | API integration + OCR tests | Client expects `/ocr` (`ocr_service.dart`) | Backend `/ocr` implementation and tests |
| REQ-03 | System shall provide structured text blocks in reading order | high | Schema + ordering tests | `OcrResponse.blocks` model exists | Backend block extraction/output |
| REQ-04 | System shall read extracted text aloud | high | Device functional test | `tts_service.dart::speak` | Usability/performance measurements |
| REQ-05 | System shall support accessible navigation across content units | high | Task-based usability tests | Not found | Navigation UI + validated results |
| REQ-06 | System shall report OCR uncertainty/errors accessibly | medium | Error-path tests + UX review | Generic error announcements exist | Confidence-specific warnings |
| REQ-07 | System shall preserve user privacy for captured documents | high | Policy + code audit | Local-host config intent in README/config | Retention policy, consent UI, secure transport strategy |
| REQ-08 | System shall be evaluated against a baseline | high | Experimental protocol + metrics | Not found | Baseline implementation and result tables |
| REQ-09 | System shall provide reproducible setup/evaluation instructions | high | Reproduction by independent user | README setup exists | Updated, complete, validated reproducibility pack |

## Limitations and threats to validity
- Current checkout does not include OCR backend path, limiting end-to-end claims.
- Accessibility conclusions are currently design-level, not user-study validated.
- README-code mismatch threatens construct validity unless reconciled.
