import cv2

img = cv2.imread("game-tree.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        h, s, v = hsv[y, x]
        print(f"Clicked at ({x}, {y}) — HSV: ({h}, {s}, {v})")

cv2.imshow("Click on the tree", img)
cv2.setMouseCallback("Click on the tree", on_click)
cv2.waitKey(0)
cv2.destroyAllWindows()