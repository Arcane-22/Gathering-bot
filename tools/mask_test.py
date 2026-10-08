import cv2
import numpy as np

img = cv2.imread("game-tree.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = np.array([28, 110, 5])
upper_green = np.array([46, 255, 60])
mask = cv2.inRange(hsv, lower_green, upper_green)

cv2.imshow("Tree Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()