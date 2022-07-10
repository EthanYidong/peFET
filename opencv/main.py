import numpy as np
import imutils
import cv2

path = r'test_images/no_test.jpg'
output = r'output_images/no_test.jpg'

# path = r'test_images/no_test.jpg'
img = cv2.imread(path, cv2.IMREAD_COLOR)
blur = cv2.GaussianBlur(img, (5,5), 1)
hsv_img = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

# Edge detection
edges = cv2.Canny(img, 100, 200)

# HSV range filter
lower_yellow = np.array([12, 20, 100])
upper_yellow = np.array([30, 255, 255])

mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

kclose = np.ones((5,5), dtype=np.uint8)
kopen = np.ones((5,5), dtype=np.uint8)
closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kclose, iterations=2)
opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kopen, iterations=6)
opening = cv2.GaussianBlur(opening, (3,3), 1)

final_mask = opening
masked_img = cv2.bitwise_and(img, img, mask=final_mask)

cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
hull = cv2.convexHull(c, False)

cv2.drawContours(masked_img, [c], -1, (0, 0, 255), 2)
cv2.drawContours(masked_img, [hull], -1, (0, 255, 0), 2)

contour_mask = np.zeros(img.shape[:2], dtype=np.uint8) 
cv2.drawContours(contour_mask, [hull], -1, (255, 0, 0), cv2.FILLED)
contour_masked_img = cv2.bitwise_and(img, img, mask=contour_mask)

test_mask = cv2.bitwise_and(cv2.bitwise_not(final_mask), contour_mask)
opening_test_mask = cv2.morphologyEx(test_mask, cv2.MORPH_OPEN, kopen, iterations=6)
final_test_mask = opening_test_mask
test_masked_img = cv2.bitwise_and(img, img, mask=opening_test_mask)

cv2.imshow("image", img)
#cv2.imshow("hsv", hsv_img)
#cv2.imshow("edges", edges)
#cv2.imshow("mask", final_mask)
#cv2.imshow("masked_img", masked_img)
#cv2.imshow("contour_masked_img", contour_masked_img)
cv2.imshow("test_masked_img", test_masked_img)

cv2.imwrite(output, test_masked_img)
cv2.waitKey(0)

cv2.destroyAllWindows()
