from pydantic import BaseModel
from typing import List, Optional


class TextBlock(BaseModel):
    index: int
    text: str
    confidence: Optional[float]


class OCRResponse(BaseModel):
    status: str
    engine: str
    blocks: List[TextBlock]
    full_text: str


class BatchOCRRequest(BaseModel):
    image_paths: List[str]
    engine: str = "easyocr"
