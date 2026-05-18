import os
from fastapi import FastAPI, File, UploadFile, Query, HTTPException

from layout import detect_text_regions
from ocr_engine import run_easyocr, run_tesseract
from schemas import OCRResponse, TextBlock, BatchOCRRequest

app = FastAPI()

SUPPORTED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ocr", response_model=OCRResponse)
async def ocr_single(
    file: UploadFile = File(...),
    engine: str = Query(default="easyocr", pattern="^(easyocr|tesseract)$"),
):
    if file.content_type not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported format '{file.content_type}'. Use JPEG or PNG.",
        )

    image_bytes = await file.read()

    if len(image_bytes) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds 10 MB limit.")

    return _process_image(image_bytes, engine)


@app.post("/ocr/batch")
def ocr_batch(request: BatchOCRRequest):
    responses = []
    for path in request.image_paths:
        if not os.path.isfile(path):
            responses.append(
                OCRResponse(
                    status="error",
                    engine=request.engine,
                    blocks=[],
                    full_text=f"File not found: {path}",
                ).dict()
            )
            continue
        with open(path, "rb") as f:
            image_bytes = f.read()
        responses.append(_process_image(image_bytes, request.engine).dict())
    return responses


def _process_image(image_bytes: bytes, engine: str) -> OCRResponse:
    bboxes = detect_text_regions(image_bytes)

    if not bboxes:
        return OCRResponse(
            status="no_text_detected",
            engine=engine,
            blocks=[],
            full_text="",
        )

    try:
        if engine == "tesseract":
            try:
                raw = run_tesseract(image_bytes, bboxes)
            except RuntimeError as e:
                if "not installed" in str(e).lower():
                    raise HTTPException(
                        status_code=503,
                        detail="Tesseract is not installed on this system.",
                    )
                raise
        else:
            raw = run_easyocr(image_bytes, bboxes)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR error: {str(e)}")

    blocks = [
        TextBlock(index=i, text=text, confidence=conf)
        for i, (text, conf) in enumerate(raw)
        if text.strip()
    ]
    full_text = "\n".join(b.text for b in blocks)

    return OCRResponse(
        status="ok",
        engine=engine,
        blocks=blocks,
        full_text=full_text,
    )
