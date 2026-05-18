# Literature Research Targets (Questions Only)

## OCR engines and document AI
1. For mobile-captured document photos (not flat scans), which OCR engines currently provide the best CER/WER under blur, perspective distortion, and uneven lighting?
2. What hybrid pipelines (classical preprocessing + OCR model) are most effective for low-resource academic prototypes?
3. How do EasyOCR and Tesseract compare in multilingual robustness and confidence calibration for accessibility-critical reading tasks?

## PDF parsing and layout analysis
1. What lightweight methods can reconstruct reading order for multi-column or form-like documents when full document-AI models are unavailable?
2. Which open-source layout analysis tools are easiest to integrate into a Python FastAPI backend for block-level extraction?
3. What evaluation metrics are recommended for reading-order correctness and region segmentation quality in document understanding research?

## Assistive technologies for visually impaired users
1. What interaction patterns are most effective for non-visual navigation of structured documents on smartphones?
2. Which UX guidelines exist for announcing OCR uncertainty without causing cognitive overload for blind or low-vision users?
3. What evidence-based design choices improve trust and error recovery in assistive OCR tools?

## Accessible audio navigation
1. What are best practices for chunking long OCR text into navigable audio units (line/sentence/block/section)?
2. Which TTS control sets (pause/resume/repeat/skip rate/voice) have strongest usability evidence for document tasks?
3. How should accessible systems signal context transitions (e.g., heading/table/body) in spoken output?

## Evaluation methodology
1. What minimum dataset size and composition is acceptable for a course-level but rigorous OCR accessibility prototype evaluation?
2. Which metrics and statistical tests are commonly used for comparing assistive reading workflows (baseline vs enhanced navigation)?
3. How do recent papers combine objective OCR metrics with user-task performance for accessible document systems?

## Privacy and ethics
1. What privacy-by-design patterns are recommended for camera-captured document processing in assistive apps?
2. How do academic accessibility papers handle consent, sensitive-content handling, and misuse risk statements?
3. What ethical risk taxonomies are used for assistive AI systems that may produce incorrect outputs?

## Related work for IEEE framing
1. What are the closest peer-reviewed systems combining OCR, layout understanding, and audio navigation for visually impaired users?
2. Which papers provide strong baseline definitions suitable for fair comparison with simple OCR-readout systems?
3. What contribution framing is credible when a prototype has partial implementation but clear evaluation roadmap?
