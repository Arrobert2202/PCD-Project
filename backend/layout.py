import cv2
import numpy as np
from typing import List, Tuple

BBox = Tuple[int, int, int, int]  # (x, y, w, h)


def detect_text_regions(image_bytes: bytes) -> List[BBox]:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=15, C=4
    )

    # merge nearby characters into word/line blobs
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    bboxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 20 and h > 8:
            bboxes.append((x, y, w, h))

    return sort_reading_order(bboxes)


def sort_reading_order(bboxes: List[BBox]) -> List[BBox]:
    if not bboxes:
        return []

    sorted_boxes = sorted(bboxes, key=lambda b: (b[1], b[0]))

    if len(sorted_boxes) == 1:
        return sorted_boxes

    heights = [b[3] for b in sorted_boxes]
    median_h = float(np.median(heights))
    line_threshold = median_h * 0.6

    lines: List[List[BBox]] = []
    current_line: List[BBox] = [sorted_boxes[0]]

    for box in sorted_boxes[1:]:
        prev = current_line[-1]
        prev_center_y = prev[1] + prev[3] / 2
        curr_center_y = box[1] + box[3] / 2
        if abs(curr_center_y - prev_center_y) <= line_threshold:
            current_line.append(box)
        else:
            lines.append(sorted(current_line, key=lambda b: b[0]))
            current_line = [box]
    lines.append(sorted(current_line, key=lambda b: b[0]))

    return [box for line in lines for box in line]
