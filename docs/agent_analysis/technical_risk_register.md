# Technical Risk Register

| Risk | Cause | Impact | Probability | Severity | Detection method | Mitigation | Fallback plan |
|---|---|---|---|---|---|---|---|
| OCR accuracy too low | Real-world image quality + limited preprocessing | Poor readability, user frustration | high | critical | CER/WER on fixed dataset | Add preprocessing, model tuning, confidence handling | Restrict scope to document types with acceptable quality |
| Layout extraction weak | No current layout implementation | Navigation unusable for complex docs | high | critical | Manual reading-order audit + block metrics | Implement block detection and ordering heuristics | Fall back to linear text with explicit limitation |
| PDF support incomplete | No PDF ingestion path in current code | Project requirement coverage gap | medium | major | Feature matrix checks + tests | Add PDF-to-image/text ingestion module | State image-only scope in evaluation/paper |
| Inaccessible UI interactions | Navigation features not implemented | Visually impaired users cannot efficiently use tool | high | critical | Accessibility task tests, heuristic review | Add block navigation + semantic announcements | Provide simplified guided mode |
| No meaningful audio navigation | Only full-text monologue currently | Hard to find specific information | high | major | Usability tasks (find field quickly) | Add chunked playback + controls | Repeat/search by keyword as interim |
| No baseline comparison | Evaluation pipeline absent | Weak scientific validity | high | critical | Checklist audit before report | Implement simple OCR-only baseline | Use manual workflow comparator with clear caveats |
| No evaluation data | Missing dataset/ground truth in repo | Cannot quantify performance | high | critical | Repository audit for `eval/` artifacts | Create small labeled dataset with protocol | Pilot-only qualitative evaluation |
| Privacy leakage | Plain HTTP + missing policy/consent | Ethical/compliance risk | medium | major | Security/privacy review checklist | Add consent, retention policy, secure transport guidance | Restrict to offline local demo settings |
| Dependency installation failures | Heavy OCR dependencies (EasyOCR/OpenCV/Tesseract) | Setup delays, reproducibility issues | medium | major | Fresh-environment install test | Pin versions, add platform setup docs | Provide containerized or reduced dependency profile |
| Scope too large for remaining time | Multiple major missing modules | Incomplete project delivery | high | critical | Weekly milestone tracking | Prioritize MVP: OCR endpoint + baseline + evaluation | Narrow contributions and explicitly state exclusions |
