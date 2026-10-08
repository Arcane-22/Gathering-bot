import cv2
import numpy as np

img = cv2.imread("game-tree.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([28, 110, 5])
upper_green = np.array([46, 255, 60])
green_mask = cv2.inRange(hsv, lower_green, upper_green)

lower_brown = np.array([12, 140, 30])
upper_brown = np.array([20, 190, 100])
brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)


def has_trunk_below(brown_mask, x, y, w, h, frame_height):
    trunk_region_y1 = y + h
    trunk_region_y2 = min(y + h + 40, frame_height)
    trunk_region_x1 = x + w // 4
    trunk_region_x2 = x + (w * 3) // 4

    region = brown_mask[trunk_region_y1:trunk_region_y2, trunk_region_x1:trunk_region_x2]
    brown_pixel_count = cv2.countNonZero(region)
    return brown_pixel_count > 50


contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

MIN_AREA = 5000
MAX_AREA = 45000

best = None
best_area = 0

for c in contours:
    area = cv2.contourArea(c)
    if area < MIN_AREA or area > MAX_AREA:
        continue
    x, y, w, h = cv2.boundingRect(c)
    density = area / (w * h)
    aspect = w / h if h > 0 else 0
    if aspect < 0.6 or aspect > 1.6:
        continue
    if density < 0.3:
        continue
    if not has_trunk_below(brown_mask, x, y, w, h, img.shape[0]):
        continue

    if area > best_area:
        best = c
        best_area = area

if best is not None:
    M = cv2.moments(best)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    print(f"Tree found: area={best_area}, center=({cx}, {cy})")
    x, y, w, h = cv2.boundingRect(best)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.circle(img, (cx, cy), 6, (0, 0, 255), -1)
else:
    print("No tree with trunk found.")

cv2.imshow("Detected Tree", img)
cv2.waitKey(0)
cv2.destroyAllWindows()