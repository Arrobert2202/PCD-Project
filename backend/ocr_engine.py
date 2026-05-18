import numpy as np
import cv2
from typing import List, Tuple, Optional

# lazy-load easyocr — takes a few seconds on first call
_easyocr_reader = None


def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        _easyocr_reader = easyocr.Reader(["en"], gpu=False)
    return _easyocr_reader


def run_easyocr(
    image_bytes: bytes,
    bboxes: List[Tuple[int, int, int, int]]
) -> List[Tuple[str, Optional[float]]]:
    reader = get_easyocr_reader()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = []
    for (x, y, w, h) in bboxes:
        region = img[y:y+h, x:x+w]
        if region.size == 0:
            results.append(("", 0.0))
            continue
        ocr_result = reader.readtext(region)
        if ocr_result:
            text = " ".join([r[1] for r in ocr_result])
            confidence = float(np.mean([r[2] for r in ocr_result]))
        else:
            text, confidence = "", 0.0
        results.append((text, confidence))
    return results


def run_tesseract(
    image_bytes: bytes,
    bboxes: List[Tuple[int, int, int, int]]
) -> List[Tuple[str, None]]:
    try:
        import pytesseract
    except ImportError:
        raise RuntimeError("pytesseract is not installed")

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = []
    for (x, y, w, h) in bboxes:
        region = img[y:y+h, x:x+w]
        if region.size == 0:
            results.append(("", None))
            continue
        text = pytesseract.image_to_string(region, lang="eng").strip()
        results.append((text, None))
    return results
