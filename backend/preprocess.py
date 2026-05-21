import math
import os
import cv2
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

_DEBUG = os.environ.get("OCR_DEBUG", "0") == "1"
_DEBUG_DIR = Path(__file__).parent / "debug"
_MAX_WORKING_SIDE = int(os.environ.get("OCR_MAX_WORKING_SIDE", "1800"))
_MAX_WORKING_PIXELS = int(os.environ.get("OCR_MAX_WORKING_PIXELS", "2500000"))
_JPEG_QUALITY = int(os.environ.get("OCR_PREPROCESS_JPEG_QUALITY", "85"))


@dataclass
class PreprocessTransform:
    """Records every coordinate-changing step so OCR bboxes (in preprocessed
    space) can be mapped back to original image space.

    Transform order:
      1. normalize_scale  — one resize that handles both shrink and grow
      2. deskew           — rotation around image centre

    Inverse order to recover original coords:
      undo deskew → undo scale
    """
    scale_factor: float     # combined scale applied to the image; 1 = no-op
    deskew_angle: float     # degrees passed to getRotationMatrix2D; 0 = no-op
    deskew_center_x: float  # rotation centre in the scaled image
    deskew_center_y: float

    def bbox_to_original(
        self, x: int, y: int, w: int, h: int
    ) -> Tuple[int, int, int, int]:
        fx, fy, fw, fh = float(x), float(y), float(w), float(h)

        # 1. undo deskew: rotate all four corners by -angle, then re-bbox
        if self.deskew_angle != 0.0:
            corners = [
                (fx,      fy     ),
                (fx + fw, fy     ),
                (fx + fw, fy + fh),
                (fx,      fy + fh),
            ]
            cx, cy = self.deskew_center_x, self.deskew_center_y
            rotated = [_rotate_point(px, py, cx, cy, -self.deskew_angle)
                       for px, py in corners]
            xs = [p[0] for p in rotated]
            ys = [p[1] for p in rotated]
            fx, fy = min(xs), min(ys)
            fw, fh = max(xs) - fx, max(ys) - fy

        # 2. undo scale
        f = self.scale_factor
        return (
            int(round(fx / f)),
            int(round(fy / f)),
            int(round(fw / f)),
            int(round(fh / f)),
        )


def _rotate_point(
    x: float, y: float, cx: float, cy: float, angle_deg: float
) -> Tuple[float, float]:
    a = math.radians(angle_deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    dx, dy = x - cx, y - cy
    return cx + dx * cos_a - dy * sin_a, cy + dx * sin_a + dy * cos_a


def preprocess_image(
    image_bytes: bytes,
) -> Tuple[bytes, PreprocessTransform]:
    img = _decode_image(image_bytes)

    img, scale_factor = _normalize_scale(img)
    img, deskew_angle, deskew_center = _deskew(img)
    _dbg(img, "deskewed")

    transform = PreprocessTransform(
        scale_factor=scale_factor,
        deskew_angle=deskew_angle,
        deskew_center_x=deskew_center[0],
        deskew_center_y=deskew_center[1],
    )
    return _encode_jpeg(img), transform


def _decode_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image data.")
    return img


def _encode_jpeg(img: np.ndarray) -> bytes:
    ok, buf = cv2.imencode(
        ".jpg", img,
        [int(cv2.IMWRITE_JPEG_QUALITY), _JPEG_QUALITY],
    )
    if not ok:
        raise ValueError("Could not encode preprocessed image.")
    return buf.tobytes()


def _normalize_scale(
    img: np.ndarray,
    target_char_height: int = 32,
) -> Tuple[np.ndarray, float]:
    """Scale the image so character height lands near target_char_height px,
    while keeping the longest side within _MAX_WORKING_SIDE and total pixels
    within _MAX_WORKING_PIXELS.  Works in both directions (shrink and grow)."""
    h, w = img.shape[:2]

    # Start from character-height estimate
    factor = 1.0
    median_h = _estimate_char_height(img)
    if median_h is not None and median_h > 0:
        factor = target_char_height / median_h
        factor = min(factor, 6.0)   # never enlarge more than 6×
        factor = max(factor, 1 / 6) # never shrink more than 6×

    # Clamp by max side length
    if _MAX_WORKING_SIDE > 0:
        projected_side = max(h, w) * factor
        if projected_side > _MAX_WORKING_SIDE:
            factor *= _MAX_WORKING_SIDE / projected_side

    # Clamp by max pixel count
    if _MAX_WORKING_PIXELS > 0:
        projected_pixels = (h * factor) * (w * factor)
        if projected_pixels > _MAX_WORKING_PIXELS:
            factor *= math.sqrt(_MAX_WORKING_PIXELS / projected_pixels)

    if abs(factor - 1.0) < 0.05:
        return img, 1.0

    interp = cv2.INTER_LANCZOS4 if factor >= 1.0 else cv2.INTER_AREA
    new_w = max(1, int(round(w * factor)))
    new_h = max(1, int(round(h * factor)))
    return cv2.resize(img, (new_w, new_h), interpolation=interp), factor


def _estimate_char_height(img: np.ndarray) -> Optional[float]:
    """Return the median height of character-shaped connected components."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )
    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(
        thresh, connectivity=8
    )
    if num_labels < 2:
        return None

    img_h, img_w = img.shape[:2]
    heights = []
    for i in range(1, num_labels):
        comp_h = int(stats[i, cv2.CC_STAT_HEIGHT])
        comp_w = int(stats[i, cv2.CC_STAT_WIDTH])
        area   = int(stats[i, cv2.CC_STAT_AREA])

        if area < 10:                      # noise
            continue
        if comp_h < 4:                     # too short to be a character
            continue
        if comp_h > img_h * 0.25:         # taller than 25% of image — not a char
            continue
        if comp_w > img_w * 0.6:          # nearly full-width — rule / border
            continue
        if comp_h / max(comp_w, 1) > 8:   # extreme aspect ratio — vertical line
            continue

        heights.append(comp_h)

    if len(heights) < 5:
        return None
    return float(np.median(heights))


def _deskew(
    img: np.ndarray, max_angle: float = 15.0
) -> Tuple[np.ndarray, float, Tuple[float, float]]:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )[1]
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 10:
        return img, 0.0, (0.0, 0.0)

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = 90 + angle
    if abs(angle) > max_angle:
        return img, 0.0, (0.0, 0.0)

    h, w = img.shape[:2]
    cx, cy = w / 2.0, h / 2.0
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return rotated, angle, (cx, cy)


def _dbg(img: np.ndarray, name: str) -> None:
    if not _DEBUG:
        return
    _DEBUG_DIR.mkdir(exist_ok=True)
    cv2.imwrite(str(_DEBUG_DIR / f"{name}.png"), img)


def dbg_boxes(image_bytes: bytes, raw: list) -> None:
    if not _DEBUG:
        return
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return
    for text, _, b in raw:
        if b and text.strip():
            x, y, w, h = b
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    _dbg(img, "ocr_boxes")
