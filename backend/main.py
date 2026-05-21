import base64
from typing import Optional, Tuple
from fastapi import FastAPI, HTTPException
from jiwer import process_words, process_characters

from fuzzy import apply_fuzzy_matching
from layout import detect_text_regions
from ocr_engine import run_easyocr, run_tesseract, run_paddleocr
from preprocess import preprocess_image, dbg_boxes
from schemas import (
    OCRRequest, OCRResponse, TextBlock, BoundingBox,
    BatchOCRRequest,
    EvaluateRequest, EvaluateResponse, ErrorCounts,
    BatchEvaluateRequest, BatchEvaluateResponse, AggregateMetrics,
)

app = FastAPI()

MAX_SIZE = 10 * 1024 * 1024  # 10 MB
_JPEG_MAGIC = b"\xff\xd8"
_PNG_MAGIC = b"\x89PNG"

_lingua_detector = None


def get_lingua_detector():
    global _lingua_detector
    if _lingua_detector is None:
        from lingua import LanguageDetectorBuilder
        _lingua_detector = LanguageDetectorBuilder.from_all_languages().build()
    return _lingua_detector


def detect_language(text: str) -> Optional[str]:
    if not text.strip():
        return None
    try:
        result = get_lingua_detector().detect_language_of(text)
        if result is None:
            return None
        return result.iso_code_639_1.name.lower()
    except Exception:
        return None


def _decode_image(image_b64: str) -> bytes:
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]
    try:
        data = base64.b64decode(image_b64)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid base64 image data.")
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Image exceeds 10 MB limit.")
    if not (data[:2] == _JPEG_MAGIC or data[:4] == _PNG_MAGIC):
        raise HTTPException(status_code=422, detail="Unsupported format. Use JPEG or PNG.")
    return data


def _compute_metrics(
    expected: str, hypothesis: str
) -> Tuple[Optional[float], Optional[float], Optional[ErrorCounts], Optional[ErrorCounts]]:
    if not expected.strip():
        return None, None, None, None
    try:
        word_out = process_words(expected, hypothesis)
        char_out = process_characters(expected, hypothesis)
        return (
            round(word_out.wer, 4),
            round(char_out.cer, 4),
            ErrorCounts(
                substitutions=word_out.substitutions,
                insertions=word_out.insertions,
                deletions=word_out.deletions,
                hits=word_out.hits,
            ),
            ErrorCounts(
                substitutions=char_out.substitutions,
                insertions=char_out.insertions,
                deletions=char_out.deletions,
                hits=char_out.hits,
            ),
        )
    except Exception:
        return None, None, None, None


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ocr", response_model=OCRResponse)
def ocr_single(request: OCRRequest):
    image_bytes = _decode_image(request.image)
    return _process_image(image_bytes, request.engine, request.lang, request.fuzzy, request.fuzzer)


@app.post("/ocr/batch")
def ocr_batch(request: BatchOCRRequest):
    responses = []
    for image_b64 in request.images:
        try:
            image_bytes = _decode_image(image_b64)
        except HTTPException as e:
            responses.append(
                OCRResponse(
                    status="error",
                    engine=request.engine,
                    blocks=[],
                    full_text=e.detail,
                ).dict()
            )
            continue
        responses.append(_process_image(image_bytes, request.engine, request.lang, request.fuzzy, request.fuzzer).dict())
    return responses


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_single(request: EvaluateRequest):
    image_bytes = _decode_image(request.image)
    ocr = _process_image(image_bytes, request.engine, request.lang, request.fuzzy, request.fuzzer)
    wer, cer, word_errors, char_errors = _compute_metrics(request.expected_text, ocr.full_text)
    return EvaluateResponse(
        status=ocr.status,
        engine=ocr.engine,
        language=ocr.language,
        full_text=ocr.full_text,
        expected_text=request.expected_text,
        wer=wer,
        cer=cer,
        word_errors=word_errors,
        char_errors=char_errors,
        blocks=ocr.blocks,
    )


@app.post("/evaluate/batch", response_model=BatchEvaluateResponse)
def evaluate_batch(request: BatchEvaluateRequest):
    results = []
    for item in request.items:
        try:
            image_bytes = _decode_image(item.image)
            ocr = _process_image(image_bytes, request.engine, request.lang, request.fuzzy, request.fuzzer)
            wer, cer, word_errors, char_errors = _compute_metrics(item.expected_text, ocr.full_text)
            results.append(EvaluateResponse(
                status=ocr.status,
                engine=ocr.engine,
                language=ocr.language,
                full_text=ocr.full_text,
                expected_text=item.expected_text,
                wer=wer,
                cer=cer,
                word_errors=word_errors,
                char_errors=char_errors,
                blocks=ocr.blocks,
            ))
        except HTTPException as e:
            results.append(EvaluateResponse(
                status="error",
                engine=request.engine,
                full_text=e.detail,
                expected_text=item.expected_text,
                blocks=[],
            ))

    valid = [r for r in results if r.wer is not None]
    aggregate = AggregateMetrics(
        mean_wer=round(sum(r.wer for r in valid) / len(valid), 4) if valid else 0.0,
        mean_cer=round(sum(r.cer for r in valid) / len(valid), 4) if valid else 0.0,
    )
    return BatchEvaluateResponse(results=results, aggregate=aggregate)


def _run_engine(engine: str, image_bytes: bytes, ocr_lang: str):
    if engine == "paddleocr":
        return run_paddleocr(image_bytes, ocr_lang)
    elif engine == "tesseract":
        try:
            return run_tesseract(image_bytes, ocr_lang)
        except RuntimeError as e:
            if "not installed" in str(e).lower():
                raise HTTPException(
                    status_code=503,
                    detail="Tesseract is not installed on this system.",
                )
            raise
    else:
        bboxes = detect_text_regions(image_bytes)
        return run_easyocr(image_bytes, bboxes, ocr_lang) if bboxes else []


def _process_image(image_bytes: bytes, engine: str, lang: str = "auto", fuzzy: bool = False, fuzzer: str = "symspell") -> OCRResponse:
    try:
        image_bytes, transform = preprocess_image(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    ocr_lang = "en" if lang == "auto" else lang

    try:
        raw = _run_engine(engine, image_bytes, ocr_lang)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {str(e)}")

    dbg_boxes(image_bytes, raw)

    resolved_lang = detect_language(" ".join(t for t, _, _ in raw if t.strip())) if lang == "auto" else lang

    blocks = []
    for i, (text, conf, b) in enumerate(raw):
        if not text.strip():
            continue
        if b:
            ox, oy, ow, oh = transform.bbox_to_original(*b)
            bbox = BoundingBox(x=ox, y=oy, width=ow, height=oh)
        else:
            bbox = None
        blocks.append(TextBlock(index=i, text=text, confidence=conf, bbox=bbox))

    if not blocks:
        return OCRResponse(
            status="no_text_detected",
            engine=engine,
            language=None,
            blocks=[],
            full_text="",
        )

    full_text = "\n".join(b.text for b in blocks)

    if fuzzy:
        blocks = [
            TextBlock(
                index=b.index,
                text=apply_fuzzy_matching(b.text, resolved_lang, fuzzer),
                confidence=b.confidence,
                bbox=b.bbox,
            )
            for b in blocks
        ]
        full_text = "\n".join(b.text for b in blocks)

    return OCRResponse(
        status="ok",
        engine=engine,
        language=resolved_lang,
        blocks=blocks,
        full_text=full_text,
    )
