import os
import numpy as np
import cv2
from typing import List, Tuple, Optional

_easyocr_readers: dict = {}
_paddle_readers: dict = {}

# ISO 639-1 → Tesseract 3-letter codes
TESSERACT_LANG_MAP = {
    "en": "eng", "ro": "ron", "fr": "fra", "de": "deu",
    "es": "spa", "it": "ita", "pt": "por", "ru": "rus",
    "zh": "chi_sim", "ja": "jpn", "ko": "kor", "ar": "ara",
    "nl": "nld", "pl": "pol", "sv": "swe", "tr": "tur",
}

# ISO 639-1 → EasyOCR lang codes
EASYOCR_LANG_MAP = {
    "en": "en", "fr": "fr", "de": "de", "es": "es", "pt": "pt",
    "it": "it", "nl": "nl", "pl": "pl", "ru": "ru", "ar": "ar",
    "zh": "ch_sim", "ja": "ja", "ko": "ko", "ro": "ro",
    "sv": "sv", "tr": "tr", "eu": "eu", "lv": "lv",
}

# ISO 639-1 → PaddleOCR lang codes
PADDLE_LANG_MAP = {
    "en": "en", "zh": "ch", "ja": "japan", "ko": "korean",
    "fr": "fr", "de": "german", "ru": "ru", "ar": "ar",
    "es": "es", "pt": "pt", "it": "it",
}


def get_easyocr_reader(lang: str = "en"):
    easyocr_lang = EASYOCR_LANG_MAP.get(lang, "en")
    if easyocr_lang not in _easyocr_readers:
        import easyocr
        _easyocr_readers[easyocr_lang] = easyocr.Reader([easyocr_lang], gpu=True)
    return _easyocr_readers[easyocr_lang]


def run_easyocr(
    image_bytes: bytes,
    bboxes: List[Tuple[int, int, int, int]],
    lang: str = "en",
) -> List[Tuple[str, Optional[float], Optional[Tuple[int, int, int, int]]]]:
    reader = get_easyocr_reader(lang)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = []
    for (x, y, w, h) in bboxes:
        region = img[y:y+h, x:x+w]
        if region.size == 0:
            results.append(("", 0.0, (x, y, w, h)))
            continue
        ocr_result = reader.readtext(region)
        if ocr_result:
            text = " ".join([r[1] for r in ocr_result])
            confidence = float(np.mean([r[2] for r in ocr_result]))
        else:
            text, confidence = "", 0.0
        results.append((text, confidence, (x, y, w, h)))
    return results


def get_paddle_reader(lang: str = "en"):
    paddle_lang = PADDLE_LANG_MAP.get(lang, "en")
    if paddle_lang not in _paddle_readers:
        from paddleocr import PaddleOCR
        _paddle_readers[paddle_lang] = PaddleOCR(
            use_angle_cls=True, lang=paddle_lang, show_log=False
        )
    return _paddle_readers[paddle_lang]


def run_paddleocr(
    image_bytes: bytes,
    lang: str = "en",
) -> List[Tuple[str, Optional[float], Optional[Tuple[int, int, int, int]]]]:
    reader = get_paddle_reader(lang)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = reader.ocr(img, cls=True)
    if not result or result[0] is None:
        return []

    out = []
    for line in result[0]:
        poly = line[0]
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        x, y = int(min(xs)), int(min(ys))
        w, h = int(max(xs)) - x, int(max(ys)) - y
        out.append((line[1][0], float(line[1][1]), (x, y, w, h)))
    return out


def _configure_tesseract(pytesseract):
    default_path = "D:/Tesseract-OCR/tesseract.exe"
    if os.name == "nt" and os.path.isfile(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path


def run_tesseract(
    image_bytes: bytes,
    lang: str = "en",
) -> List[Tuple[str, Optional[float], Optional[Tuple[int, int, int, int]]]]:
    try:
        import pytesseract
    except ImportError:
        raise RuntimeError("pytesseract is not installed")
    _configure_tesseract(pytesseract)

    tess_lang = TESSERACT_LANG_MAP.get(lang, "eng")
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    data = pytesseract.image_to_data(
        img, lang=tess_lang, config="--psm 3",
        output_type=pytesseract.Output.DICT,
    )

    # group word-level entries (level==5) into lines
    line_groups: dict = {}
    for i, level in enumerate(data["level"]):
        if level != 5 or not data["text"][i].strip():
            continue
        key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
        line_groups.setdefault(key, []).append(i)

    results = []
    for key in sorted(line_groups):
        indices = line_groups[key]
        line_text = " ".join(data["text"][i].strip() for i in indices)
        x = min(data["left"][i] for i in indices)
        y = min(data["top"][i] for i in indices)
        x2 = max(data["left"][i] + data["width"][i] for i in indices)
        y2 = max(data["top"][i] + data["height"][i] for i in indices)
        conf_vals = [data["conf"][i] for i in indices if data["conf"][i] >= 0]
        conf = float(np.mean(conf_vals)) / 100.0 if conf_vals else None
        results.append((line_text, conf, (x, y, x2 - x, y2 - y)))
    return results
