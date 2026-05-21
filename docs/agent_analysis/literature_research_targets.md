# Literature Research Targets (Questions for ChatGPT Deep Research)

> Do not answer here; these are targeted research questions.

## OCR engines and document AI
1. For receipt-like noisy mobile captures, how do EasyOCR, Tesseract, and PaddleOCR compare in peer-reviewed benchmarks (accuracy vs latency vs hardware)?
2. What preprocessing strategies most improve OCR robustness under blur/skew/low-contrast for mobile document photos?
3. What recent lightweight OCR/document-AI models are suitable for near-real-time local inference on consumer hardware?
4. What are best practices for multilingual OCR when language detection is uncertain or mixed within one document?

## PDF parsing and layout analysis
1. What methods best reconstruct reading order in multi-column, table-heavy, or form-like documents?
2. Which open-source pipelines provide strong document layout parsing from images and from native PDFs, and how are they evaluated?
3. What metrics are standard for layout extraction quality (bbox, ordering, structural tags), and what benchmark datasets are recommended?
4. How should one evaluate reading-order correctness for accessibility-focused document navigation?

## Assistive technologies for visually impaired users
1. What interaction patterns are most effective for blind/low-vision users in document-reading apps (block navigation, heading jumps, summaries)?
2. What usability metrics and study protocols are commonly used for accessibility-focused OCR systems?
3. What evidence exists on cognitive load and trust when OCR errors are not explicitly communicated to users?
4. What are established design guidelines for uncertainty communication in assistive reading tools?

## Accessible audio navigation
1. Which TTS navigation paradigms (linear, hierarchical, spatial, confidence-aware) perform best for scanned document consumption?
2. How should systems map visual layout regions to audio navigation units for comprehension?
3. What strategies improve multilingual TTS alignment with OCR-detected language in mixed-language documents?
4. What are recommended fallback behaviors when OCR confidence is low or text is missing?

## Evaluation methodology
1. What constitutes a credible baseline for accessible OCR prototypes in academic evaluations?
2. How many documents/users are typically needed for meaningful pilot-level evidence in this domain?
3. Which statistical tests are appropriate for paired OCR metric comparisons across engines and preprocessing variants?
4. How should failure-case analysis (blur, skew, occlusion) be reported to avoid overstated claims?

## Privacy and ethics
1. What privacy threat models are recommended for mobile-captured sensitive documents in local/LAN OCR architectures?
2. What logging minimization/redaction practices are considered acceptable for OCR research prototypes?
3. What consent language is recommended in assistive document apps to balance utility and risk awareness?
4. What fairness and accessibility bias concerns are documented for multilingual OCR + TTS systems?

## Related work for IEEE framing
1. Which recent IEEE/ACM papers directly address OCR accessibility for visually impaired users, and what are their validated contributions?
2. What novelty claims are realistic for a project combining known OCR engines with accessibility-focused interaction design?
3. How do strong papers in this area structure the integrated specification/requirements traceability section?
4. What common limitations and threats-to-validity statements appear in accepted papers on accessible document understanding?
