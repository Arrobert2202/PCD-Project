import os
import cv2
import numpy as np
from pathlib import Path

_DEBUG = os.environ.get("OCR_DEBUG", "0") == "1"
_DEBUG_DIR = Path(__file__).parent / "debug"


def preprocess_image(image_bytes: bytes) -> bytes:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img = _upscale_if_small(img)
    img = _deskew(img)
    img = _enhance_contrast(img)
    img = _crop_to_content(img)
    _dbg(img, "cropped")

    _, buf = cv2.imencode(".png", img)
    return buf.tobytes()


def _dbg(img: np.ndarray, name: str) -> None:
    _DEBUG_DIR.mkdir(exist_ok=True)
    cv2.imwrite(str(_DEBUG_DIR / f"{name}.png"), img)


def dbg_boxes(image_bytes: bytes, raw: list) -> None:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    for text, _, b in raw:
        if b and text.strip():
            x, y, w, h = b
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    _dbg(img, "ocr_boxes")



def _crop_to_content(img: np.ndarray, padding: int = 20) -> np.ndarray:
    try:
        import pytesseract
    except ImportError:
        return img

    tess_exe = "D:/Tesseract-OCR/tesseract.exe"
    if os.name == "nt" and os.path.isfile(tess_exe):
        pytesseract.pytesseract.tesseract_cmd = tess_exe

    data = pytesseract.image_to_data(
        img, lang="eng", config="--psm 11",
        output_type=pytesseract.Output.DICT,
    )

    boxes = [
        (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
        for i in range(len(data["text"]))
        if data["text"][i].strip() and int(data["conf"][i]) > 0
    ]

    if not boxes:
        return img

    h_img, w_img = img.shape[:2]
    x1 = max(0, min(x for x, _, _, _ in boxes) - padding)
    y1 = max(0, min(y for _, y, _, _ in boxes) - padding)
    x2 = min(w_img, max(x + w for x, _, w, _ in boxes) + padding)
    y2 = min(h_img, max(y + h for _, y, _, h in boxes) + padding)

    cropped = img[y1:y2, x1:x2]
    return cropped if cropped.size > 0 else img


def _upscale_if_small(img: np.ndarray, min_side: int = 600) -> np.ndarray:
    h, w = img.shape[:2]
    if min(h, w) < min_side:
        scale = min_side / min(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
    return img


def _deskew(img: np.ndarray, max_angle: float = 15.0) -> np.ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 10:
        return img
    angle = cv2.minAreaRect(coords)[-1]
    # minAreaRect returns angle in [-90, 0); nudge into [-45, 45) range
    if angle < -45:
        angle = 90 + angle
    if abs(angle) > max_angle:
        return img
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def _enhance_contrast(img: np.ndarray) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    lab = cv2.merge([clahe.apply(l), a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

