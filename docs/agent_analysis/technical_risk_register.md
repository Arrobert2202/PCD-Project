# Technical Risk Register

| Risk | Cause | Impact | Probability | Severity | Detection method | Mitigation | Fallback plan |
|---|---|---|---|---|---|---|---|
| OCR accuracy too low | Difficult images, engine limitations, weak preprocessing | Poor user trust/usability | medium | high | WER/CER trend and failure-case review | tune preprocessing/engine by doc type | constrain supported doc types and disclose limits |
| Layout extraction weak | Simple contour + heuristic ordering | Incorrect reading sequence | high | high | manual ordering audit on test set | improve ordering heuristics, add block typing | allow user manual next/prev reorder flow |
| PDF support incomplete | UI allows PDF but backend rejects | Broken user journeys | high | high | end-to-end upload tests for PDF | implement PDF rasterization or remove PDF option | show explicit unsupported-format message |
| Inaccessible UI in edge cases | Limited formal accessibility QA | target users blocked from key tasks | medium | high | accessibility task walkthroughs | add focus/announcement/error recovery improvements | provide simplified “audio-first mode” |
| No meaningful audio navigation | Current navigation mostly tap-based blocks/read-all | limited efficiency for blind users | medium | high | user task completion metrics | add structured navigation controls and shortcuts | fallback to linear read with indexed commands |
| No baseline comparison evidence | Benchmark exists but no committed results | weak academic claims | medium | high | paper evidence checklist | run and commit baseline/proposed results | restrict claims to qualitative prototype |
| No evaluation data package | No in-repo annotated dataset subset | low reproducibility | high | high | clean-room rerun attempt | add small versioned eval pack + scripts | include exact external download recipe |
| Privacy leakage | Debug image files persisted | exposure of sensitive documents | medium | critical | inspect filesystem after OCR calls | disable debug writes by default, add deletion controls | run in ephemeral environment only |
| Dependency installation failures | Heavy OCR deps and platform specifics | blocked replication/demo | medium | major | fresh environment install test | document platform-specific setup and alternatives | provide one-engine minimal mode |
| Scope too large for remaining time | OCR + accessibility + evaluation + paper tasks | unfinished deliverables | high | major | milestone burndown tracking | prioritize core requirements and report limits | reduce optional features and focus on evaluation |
