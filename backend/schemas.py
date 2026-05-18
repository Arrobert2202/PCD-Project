from pydantic import BaseModel
from typing import List, Optional, Literal


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class TextBlock(BaseModel):
    index: int
    text: str
    confidence: Optional[float]
    bbox: Optional[BoundingBox] = None


class OCRRequest(BaseModel):
    image: str  # base64-encoded JPEG or PNG
    engine: Literal["easyocr", "tesseract", "paddleocr"] = "easyocr"
    lang: str = "auto"
    fuzzy: bool = False
    fuzzer: Literal["symspell", "pyspellchecker"] = "symspell"


class BatchOCRRequest(BaseModel):
    images: List[str]  # base64-encoded JPEG or PNG images
    engine: Literal["easyocr", "tesseract", "paddleocr"] = "easyocr"
    lang: str = "auto"
    fuzzy: bool = False
    fuzzer: Literal["symspell", "pyspellchecker"] = "symspell"


class OCRResponse(BaseModel):
    status: str
    engine: str
    language: Optional[str] = None
    blocks: List[TextBlock]
    full_text: str


class ErrorCounts(BaseModel):
    substitutions: int
    insertions: int
    deletions: int
    hits: int


class EvaluateRequest(BaseModel):
    image: str  # base64-encoded JPEG or PNG
    expected_text: str
    engine: Literal["easyocr", "tesseract", "paddleocr"] = "easyocr"
    lang: str = "auto"
    fuzzy: bool = False
    fuzzer: Literal["symspell", "pyspellchecker"] = "symspell"


class EvaluateResponse(BaseModel):
    status: str
    engine: str
    language: Optional[str] = None
    full_text: str
    expected_text: str
    wer: Optional[float] = None
    cer: Optional[float] = None
    word_errors: Optional[ErrorCounts] = None
    char_errors: Optional[ErrorCounts] = None
    blocks: List[TextBlock]


class BatchEvaluateItem(BaseModel):
    image: str
    expected_text: str


class BatchEvaluateRequest(BaseModel):
    items: List[BatchEvaluateItem]
    engine: Literal["easyocr", "tesseract", "paddleocr"] = "easyocr"
    lang: str = "auto"
    fuzzy: bool = False
    fuzzer: Literal["symspell", "pyspellchecker"] = "symspell"


class AggregateMetrics(BaseModel):
    mean_wer: float
    mean_cer: float


class BatchEvaluateResponse(BaseModel):
    results: List[EvaluateResponse]
    aggregate: AggregateMetrics
