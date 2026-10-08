import cv2
import numpy as np
import random
from config import (
    LOWER_GREEN, UPPER_GREEN, LOWER_BROWN, UPPER_BROWN,
    MIN_AREA, MAX_AREA, MIN_DENSITY, MIN_ASPECT, MAX_ASPECT,
    TRUNK_SEARCH_HEIGHT, MIN_TRUNK_PIXELS
)

def has_trunk_below(brown_mask, x, y, w, h, frame_height):
    y1 = y + h
    y2 = min(y + h + TRUNK_SEARCH_HEIGHT, frame_height)
    x1 = x + w // 4
    x2 = x + (w * 3) // 4
    region = brown_mask[y1:y2, x1:x2]
    return cv2.countNonZero(region) > MIN_TRUNK_PIXELS


def find_tree(frame_bgr):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, np.array(LOWER_GREEN), np.array(UPPER_GREEN))
    brown_mask = cv2.inRange(hsv, np.array(LOWER_BROWN), np.array(UPPER_BROWN))

    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best = None
    best_area = 0

    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_AREA or area > MAX_AREA:
            continue
        x, y, w, h = cv2.boundingRect(c)
        density = area / (w * h)
        aspect = w / h if h > 0 else 0
        if aspect < MIN_ASPECT or aspect > MAX_ASPECT:
            continue
        if density < MIN_DENSITY:
            continue
        if not has_trunk_below(brown_mask, x, y, w, h, frame_bgr.shape[0]):
            continue
        if area > best_area:
            best = c
            best_area = area

    if best is None:
        return None

    M = cv2.moments(best)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)


def wander_click_point(frame_width, frame_height):
    x = random.randint(int(frame_width * 0.3), int(frame_width * 0.7))
    y = random.randint(int(frame_height * 0.3), int(frame_height * 0.7))
    return (x, y)