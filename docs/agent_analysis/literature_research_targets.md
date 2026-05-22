# Literature Research Targets (Questions Only)

## OCR engines and document AI

1. For low-resource mobile-assisted OCR pipelines, how do EasyOCR, Tesseract, and PaddleOCR compare on noisy handheld document images in recent peer-reviewed benchmarks?
2. Which preprocessing steps (deskew, super-resolution/upscaling, denoising, adaptive thresholding) most consistently improve OCR CER/WER for receipts and forms?
3. What recent methods improve multilingual OCR language detection and language-specific post-correction in mixed-language documents?
4. What are recommended evaluation datasets for multilingual scene/document OCR that include licensing suitable for academic publication?

## PDF parsing and layout analysis

1. What are the best lightweight approaches for reading-order reconstruction in multi-column and form-like documents without full transformer models?
2. Which open-source libraries are most reliable for converting mobile-captured PDFs into OCR-ready images while preserving page order and quality?
3. What layout metrics are commonly used to evaluate block detection/order correctness in document-understanding systems?

## Assistive technologies for visually impaired users

1. What interaction patterns are most effective for non-visual navigation of OCR text blocks on smartphones?
2. How should uncertainty/confidence be communicated in assistive OCR systems to reduce harmful over-trust?
3. Which accessibility heuristics and standards are most applicable to Flutter mobile apps targeting blind users?

## Accessible audio navigation

1. What are best practices for mapping document structure to TTS navigation units (line/block/section/page)?
2. How do users perform with “read all” vs “block-by-block” audio navigation in document reading tasks?
3. What multilingual TTS strategies are recommended when OCR language is auto-detected and may be uncertain?

## Evaluation methodology

1. What minimum sample sizes and task designs are recommended for pilot usability studies with visually impaired users in academic prototypes?
2. Which combined metric sets are considered robust for OCR+accessibility systems (accuracy, latency, usability, error recovery)?
3. How should baseline conditions be defined to avoid unfair or overstated claims in OCR prototype papers?

## Privacy and ethics

1. What privacy-by-design controls are expected for assistive document OCR apps that may process sensitive personal documents?
2. What ethical guidelines exist for communicating OCR limitations in accessibility-focused assistive tools?
3. How should local-vs-cloud processing trade-offs be reported in accessibility system papers?

## Related work for IEEE framing

1. Which recent IEEE/ACM papers best represent end-to-end assistive document reading systems (capture → OCR → navigation/audio)?
2. How do state-of-the-art systems frame contributions: OCR accuracy, interaction design, privacy, or integrated performance?
3. What common threats-to-validity sections are expected in papers on accessible OCR prototypes?
