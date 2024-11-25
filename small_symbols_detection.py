import cv2
import numpy as np

def get_small_symbol_information(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Image {image_path} not found or cannot be opened.")
        exit()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    mask_red = mask_red1 + mask_red2

    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    height, width, _ = image.shape

    roi_brake = (int(0.55 * width), int(0.05 * height), int(0.15 * width), int(0.28 * height))
    roi_seatbelt = (int(0.08 * width), int(0.46 * height), int(0.115 * width), int(0.15 * height))
    roi_left_indicator = (int(0.3 * width), int(0.1 * height), int(0.2 * width), int(0.25 * height))
    roi_right_indicator = (int(0.6 * width), int(0.1 * height), int(0.2 * width), int(0.25 * height))
    roi_fog_light = (int(0.21 * width), int(0.38 * height), int(0.07 * width), int(0.15 * height))
    roi_parking_lights = (int(0.26 * width), int(0.44 * height), int(0.07 * width), int(0.15 * height))

    def is_contour_in_roi(contour, roi):
        x, y, w, h = cv2.boundingRect(contour)
        x_roi, y_roi, w_roi, h_roi = roi
        return x_roi <= x <= x_roi + w_roi and y_roi <= y <= y_roi + h_roi

    brake_detected = False
    seatbelt_detected = False
    left_indicator_detected = False
    right_indicator_detected = False
    fog_light_detected = False
    parking_light_detected = False

    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            if is_contour_in_roi(contour, roi_brake):
                brake_detected = True
            if is_contour_in_roi(contour, roi_seatbelt):
                seatbelt_detected = True

    for contour in contours_green:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            if is_contour_in_roi(contour, roi_left_indicator):
                left_indicator_detected = True
            if is_contour_in_roi(contour, roi_right_indicator):
                right_indicator_detected = True
            if is_contour_in_roi(contour, roi_fog_light):
                fog_light_detected = True
            if is_contour_in_roi(contour, roi_parking_lights):
                parking_light_detected = True

    if brake_detected:
        print("Brake light is ON (Red).")
    else:
        print("Brake light is OFF.")

    if seatbelt_detected:
        print("Seatbelt indicator is ON (Red).")
    else:
        print("Seatbelt indicator is OFF.")

    if left_indicator_detected:
        print("Left indicator is ON (Green).")
    else:
        print("Left indicator is OFF.")

    if right_indicator_detected:
        print("Right indicator is ON (Green).")
    else:
        print("Right indicator is OFF.")

    if fog_light_detected:
        print("Fog light is ON (Green).")
    else:
        print("Fog light is OFF.")

    if parking_light_detected:
        print("Parking light is ON (Green).")
    else:
        print("Parking light is OFF.")
