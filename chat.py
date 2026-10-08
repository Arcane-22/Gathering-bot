import cv2
import numpy as np
import pytesseract
from config import TESSERACT_PATH, CHAT_REGION

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def read_chat(sct):
    frame = np.array(sct.grab(CHAT_REGION))
    frame_bgr = frame[:, :, :3]

    upscaled = cv2.resize(frame_bgr, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(upscaled, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh).lower()

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    latest_line = lines[-1] if lines else ""

    return latest_line

def chop_succeeded(text):
    return "some logs" in text

def inventory_full(text):
    return "space in" in text and "inventory" in text

def is_chopping(text):
    return "swing your axe" in text