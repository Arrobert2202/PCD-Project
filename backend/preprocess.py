import cv2
import numpy as np


def preprocess_image(image_bytes: bytes) -> bytes:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    img = _upscale_if_small(img)
    img = _deskew(img)
    img = _enhance_contrast(img)
    img = _denoise(img)

    _, buf = cv2.imencode(".png", img)
    return buf.tobytes()


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
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab = cv2.merge([clahe.apply(l), a, b])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def _denoise(img: np.ndarray) -> np.ndarray:
    return cv2.bilateralFilter(img, d=5, sigmaColor=30, sigmaSpace=30)
