from enum import Enum, auto

from cv2 import boxPoints
import numpy as np
import imutils
import cv2
import pytesseract
from PIL import Image

from .rotated_rect_crop import crop_rotated_rectangle

class TestKit(Enum):
    NOT_DETECTED = auto()
    INVALID = auto()
    POSITIVE = auto()
    NEGATIVE = auto()

KCLOSE = np.ones((5,5), dtype=np.uint8)
KOPEN = np.ones((5,5), dtype=np.uint8)

SCAN_TEXT = True

TARGET_YELLOW = [22, 123, 183]

def process_mask(mask, kclose=KCLOSE, kopen=KOPEN):
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kclose, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kopen, iterations=6)
    mask = cv2.GaussianBlur(mask, (3,3), 1)
    return mask

def points_to(line, rect):
    rX, rY, rW, rH = rect
    lX, lY, lW, lH = line

    if lW < lH:
        return (lX >= rX and lX <= rX + rW) or (lX + lW >= rX and lX + lW <= rX + rW)
    else:
        return (lY >= rY and lY <= rY + rH) or (lY + lH >= rY and lY + lH <= rY + rH)

def detect(img_data):
    img_rev = np.array(img_data.convert('RGB'))
    img = img_rev[:, :, ::-1].copy() 

    norm_img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(norm_img, (5,5), 1)
    hsv_img = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([12, 30, 100])
    upper_yellow = np.array([30, 255, 255])

    # Filter out all yellow in the image and create a mask
    yellow_mask = process_mask(cv2.inRange(hsv_img, lower_yellow, upper_yellow))

    # Find the largest area contour and the convex hull of that contour.
    yellow_contours = imutils.grab_contours(cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    largest_yellow_contour = max(yellow_contours, key=cv2.contourArea)
    largest_yellow_hull = cv2.convexHull(largest_yellow_contour, False)

    # Generate a mask for objects in the convex hull but not the contour (aka overlapping the yellow rectangle)
    contour_mask = np.zeros(norm_img.shape[:2], dtype=np.uint8) 
    cv2.drawContours(contour_mask, [largest_yellow_hull], -1, 255, cv2.FILLED)
    overlapping_mask = process_mask(cv2.bitwise_and(cv2.bitwise_not(yellow_mask), contour_mask))
    overlapping_contours = imutils.grab_contours(cv2.findContours(overlapping_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))

    largest_overlapping_contour = max(overlapping_contours, key=cv2.contourArea)
    overlapping_mask_rect = cv2.minAreaRect(largest_overlapping_contour)

    lower_grey = np.array([100, 20, 100])
    upper_grey = np.array([115, 80, 255])

    grey_mask = process_mask(cv2.inRange(hsv_img, lower_grey, upper_grey))

    grey_contours = list(imutils.grab_contours(cv2.findContours(grey_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)))
    grey_contours.sort(reverse=True, key=cv2.contourArea)
    test_rect = None
    for contour in grey_contours:
        grey_rect = cv2.minAreaRect(contour)

        _, intersection = cv2.rotatedRectangleIntersection(overlapping_mask_rect, grey_rect)
        if intersection is not None:
            test_rect = grey_rect
            break

    if test_rect is None:
        return TestKit.NOT_DETECTED
    else:
        test_img = crop_rotated_rectangle(norm_img, test_rect)
        img_len = max(test_img.shape[0], test_img.shape[1])

        gray_test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
        hsv_test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2HSV)
        
        _, threshold_test_img = cv2.threshold(gray_test_img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(threshold_test_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        lower_purple = np.array([130, 40, 120])
        upper_purple = np.array([150, 80, 255])

        purple_mask = cv2.inRange(hsv_test_img, lower_purple, upper_purple)

        purple_line_contours = list(imutils.grab_contours(cv2.findContours(purple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)))
        purple_line_contours.sort(reverse=True, key=cv2.contourArea)

        purple_lines = []

        for purple_line_contour in purple_line_contours[:2]:
            purple_lines.append(cv2.boundingRect(purple_line_contour))

        found_c = False
        found_t = False
        if SCAN_TEXT:
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w < img_len / 100 or h < img_len / 100 or w > img_len / 10 or h > img_len / 10:
                    continue

                overlaps_line = None
                for purple_line in purple_lines:
                    if points_to(purple_line, (x - 5, y - 5, w + 10, h + 10)):
                        overlaps_line = purple_line
                        break
                
                if not overlaps_line:
                    continue

                x = max(0, x - 5)
                y = max(0, y - 5)
                w = min(w + 10, test_img.shape[1] - x - 1)
                h = min(h + 10, test_img.shape[0] - y - 1)
        
                cropped = threshold_test_img[y:y + h, x:x + w].copy()

                for rot in range(4):
                    found = False
                    if rot != 0:
                        cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)

                    ocr_result = pytesseract.image_to_data(cropped, config='--psm 10', output_type=pytesseract.Output.DICT)
                    for i in range(len(ocr_result['level'])):
                        if float(ocr_result['conf'][i]) > 0.5:
                            if ocr_result['text'][i] == 'C' or ocr_result['text'][i] == 'c':
                                found_c = True
                                found = True
                            if ocr_result['text'][i] == 'T' or ocr_result['text'][i] == 't':
                                found_t = True
                                found = True     
                    if found:
                        break
        
        if not found_c:
            return TestKit.INVALID
        elif found_t:
            return TestKit.POSITIVE
        else:
            return TestKit.NEGATIVE
            
def extractTestImg(img_data):
    img_rev = np.array(img_data.convert('RGB'))
    img = img_rev[:, :, ::-1].copy() 
    norm_img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(norm_img, (5,5), 1)
    hsv_img = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([12, 30, 100])
    upper_yellow = np.array([30, 255, 255])

    # Filter out all yellow in the image and create a mask
    yellow_mask = process_mask(cv2.inRange(hsv_img, lower_yellow, upper_yellow))

    # Find the largest area contour and the convex hull of that contour.
    yellow_contours = imutils.grab_contours(cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    if not yellow_contours:
        return None
    largest_yellow_contour = max(yellow_contours, key=cv2.contourArea)
    largest_yellow_hull = cv2.convexHull(largest_yellow_contour, False)

    # Generate a mask for objects in the convex hull but not the contour (aka overlapping the yellow rectangle)
    contour_mask = np.zeros(img.shape[:2], dtype=np.uint8) 
    cv2.drawContours(contour_mask, [largest_yellow_hull], -1, 255, cv2.FILLED)

    avg_yellow = cv2.mean(hsv_img, yellow_mask)

    offset = np.full(hsv_img.shape, [TARGET_YELLOW[0] - avg_yellow[0], TARGET_YELLOW[1] - avg_yellow[1], TARGET_YELLOW[2] - avg_yellow[2]], dtype=np.int16)
    hsv_tuned_img = cv2.add(hsv_img, offset, dtype=cv2.CV_8U)
    tuned_img = cv2.cvtColor(hsv_tuned_img, cv2.COLOR_HSV2BGR)

    overlapping_mask = process_mask(cv2.bitwise_and(cv2.bitwise_not(yellow_mask), contour_mask))
    overlapping_contours = imutils.grab_contours(cv2.findContours(overlapping_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    if not overlapping_contours:
        return None
    largest_overlapping_contour = max(overlapping_contours, key=cv2.contourArea)
    overlapping_mask_rect = cv2.minAreaRect(largest_overlapping_contour)

    lower_grey = np.array([100, 20, 100])
    upper_grey = np.array([115, 120, 255])

    grey_mask = process_mask(cv2.inRange(hsv_tuned_img, lower_grey, upper_grey))
    grey_contours = list(imutils.grab_contours(cv2.findContours(grey_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)))
    grey_contours.sort(reverse=True, key=cv2.contourArea)

    test_rect = None
    for contour in grey_contours:
        grey_rect = cv2.minAreaRect(contour)

        _, intersection = cv2.rotatedRectangleIntersection(overlapping_mask_rect, grey_rect)
        if intersection is not None:
            test_rect = crop_rotated_rectangle(img, grey_rect)
    
    if test_rect is None:
        return None
    return Image.fromarray(cv2.cvtColor(test_rect, cv2.COLOR_BGR2RGB))
