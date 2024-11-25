import cv2
import numpy as np
import pytesseract
import matplotlib.pyplot as plt

def get_roi(image, x_start_percent, x_end_percent, y_start_percent, y_end_percent):
    height, width = image.shape[:2]
    x_start = int(x_start_percent * width)
    x_end = int(x_end_percent * width)
    y_start = int(y_start_percent * height)
    y_end = int(y_end_percent * height)
    return image[y_start:y_end, x_start:x_end]

def get_fuel_economy(image_path):
    image = cv2.imread(image_path)

    x_start_percent = 0.25
    x_end_percent = 0.75
    y_start_percent = 0.5
    y_end_percent = 1.0

    roi = get_roi(image, x_start_percent, x_end_percent, y_start_percent, y_end_percent)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    detection_data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)

    word_bounding_boxes = {}

    for i in range(len(detection_data['text'])):
        if int(detection_data['conf'][i]) > 60:
            word = detection_data['text'][i].lower()
            if word in ['average', 'fuel', 'economy']:
                x, y, w, h = (detection_data['left'][i],
                            detection_data['top'][i],
                            detection_data['width'][i],
                            detection_data['height'][i])
                word_bounding_boxes[word] = (x, y, w, h)

    if all(word in word_bounding_boxes for word in ['average', 'fuel', 'economy']):
        avg_coords = word_bounding_boxes['average']
        fuel_coords = word_bounding_boxes['fuel']
        eco_coords = word_bounding_boxes['economy']

        rect_x_start = min(avg_coords[0], fuel_coords[0], eco_coords[0])
        rect_y_start = min(avg_coords[1], fuel_coords[1], eco_coords[1])

        fixed_length = 650
        fixed_height = 250

        shift_up_pixels = 20
        rect_y_start = max(0, rect_y_start - shift_up_pixels)

        cv2.rectangle(roi, (rect_x_start, rect_y_start),
                    (rect_x_start + fixed_length, rect_y_start + fixed_height),
                    (255, 0, 0), 2)

        text_detection_region = roi[rect_y_start:rect_y_start + fixed_height,
                                    rect_x_start:rect_x_start + fixed_length]

        gray_text_region = cv2.cvtColor(text_detection_region, cv2.COLOR_BGR2GRAY)
        _, binary_text_region = cv2.threshold(gray_text_region, 200, 255, cv2.THRESH_BINARY_INV)
        text_detection_data = pytesseract.image_to_data(binary_text_region, output_type=pytesseract.Output.DICT)

        detected_texts = []
        exclude_words = ['average', 'fuel', 'economy', 'km', 'l', 'range', 'Range', 'tuel']

        for i in range(len(text_detection_data['text'])):
            if int(text_detection_data['conf'][i]) > 60:
                text = text_detection_data['text'][i].lower()
                if text and text not in exclude_words:
                    detected_texts.append(text)

        if len(detected_texts) == 2:
            if '.' in detected_texts[0]:
                print(f"Average fuel economy is {detected_texts[0]}{detected_texts[1]}")
            else:
                print(f"Average fuel economy is {detected_texts[0]}.{detected_texts[1]}")
        elif len(detected_texts) == 1:
            print(f"Average fuel economy is {detected_texts[0]}")
        else:
            print("Not found")

        # plt.figure(figsize=(12, 6))
        # plt.subplot(1, 2, 1)
        # plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
        # plt.title('Detected Phrase with Rectangle')
        # plt.axis('off')

        # plt.subplot(1, 2, 2)
        # plt.imshow(cv2.cvtColor(text_detection_region, cv2.COLOR_BGR2RGB))
        # plt.title('Detected Text')
        # plt.axis('off')

        # plt.show()

    else:
        print("Not all words ('average', 'fuel', 'economy') were detected.")
