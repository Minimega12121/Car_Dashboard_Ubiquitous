import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
import os

def get_middle_information(image_path):
            image = cv2.imread(image_path)


            height, width = image.shape[:2]
            lower_middle_y_start = height // 2
            lower_middle_y_end = height
            lower_middle_x_start = width // 4
            lower_middle_x_end = width * 3 // 4

            lower_middle_region = image[lower_middle_y_start:lower_middle_y_end, lower_middle_x_start:lower_middle_x_end]

            gray = cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2GRAY)

            _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

            detection_data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)

            words = []
            word_bounding_boxes = {}

            for i in range(len(detection_data['text'])):
                if int(detection_data['conf'][i]) > 60:
                    word = detection_data['text'][i].lower()
                    if word in ['average', 'economy']:
                        x, y, w, h = (detection_data['left'][i],
                                    detection_data['top'][i],
                                    detection_data['width'][i],
                                    detection_data['height'][i])
                        words.append(word)
                        word_bounding_boxes[word] = (x, y, w, h)

            average_coords = word_bounding_boxes.get('average')
            economy_coords = word_bounding_boxes.get('economy')

            if average_coords and economy_coords:
                avg_x_left = average_coords[0]
                eco_x_right = economy_coords[0] + economy_coords[2]

                for word, (x, y, w, h) in word_bounding_boxes.items():
                    cv2.rectangle(lower_middle_region, (x, y), (x + w, y + h), (0, 255, 0), 2)

                detected_letters = []

                for i in range(len(detection_data['text'])):
                    if int(detection_data['conf'][i]) > 60:
                        letter = detection_data['text'][i]
                        x, y, w, h = (detection_data['left'][i],
                                    detection_data['top'][i],
                                    detection_data['width'][i],
                                    detection_data['height'][i])

                        if avg_x_left < x < eco_x_right:
                            detected_letters.append(letter)

                # plt.figure(figsize=(12, 6))

                # plt.subplot(1, 2, 1)
                # plt.title(f'Lower Middle Region with Detected Words - {filename}')
                # plt.imshow(cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2RGB))
                # plt.axis('off')

                # plt.subplot(1, 2, 2)
                # plt.title('Binary Image')
                # plt.imshow(binary, cmap='gray')
                # plt.axis('off')

                # plt.show()

                print("Detected Words:", words)
                print("Detected Letters within the boundaries of 'average' and 'economy':", detected_letters)
            else:
                print(f"One or both words not found in image.")



# path = 'Images/'

# for filename in os.listdir(path):
#     if filename != '3.jpg': continue
#     if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
#         image_path = os.path.join(path, filename)
#         print(f'Processing image: {filename}')

#         image = cv2.imread(image_path)

#         if image is None:
#             print(f"Failed to load image: {filename}")
#             continue

#         height, width = image.shape[:2]
#         lower_middle_y_start = height // 2
#         lower_middle_y_end = height
#         lower_middle_x_start = width // 4
#         lower_middle_x_end = width * 3 // 4

#         lower_middle_region = image[lower_middle_y_start:lower_middle_y_end, lower_middle_x_start:lower_middle_x_end]

#         gray = cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2GRAY)

#         _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

#         detection_data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)

#         words = []
#         word_bounding_boxes = {}

#         for i in range(len(detection_data['text'])):
#             if int(detection_data['conf'][i]) > 60:
#                 word = detection_data['text'][i].lower()
#                 if word in ['average', 'economy']:
#                     x, y, w, h = (detection_data['left'][i],
#                                   detection_data['top'][i],
#                                   detection_data['width'][i],
#                                   detection_data['height'][i])
#                     words.append(word)
#                     word_bounding_boxes[word] = (x, y, w, h)

#         average_coords = word_bounding_boxes.get('average')
#         economy_coords = word_bounding_boxes.get('economy')

#         if average_coords and economy_coords:
#             avg_x_left = average_coords[0]
#             eco_x_right = economy_coords[0] + economy_coords[2]

#             for word, (x, y, w, h) in word_bounding_boxes.items():
#                 cv2.rectangle(lower_middle_region, (x, y), (x + w, y + h), (0, 255, 0), 2)

#             detected_letters = []

#             for i in range(len(detection_data['text'])):
#                 if int(detection_data['conf'][i]) > 60:
#                     letter = detection_data['text'][i]
#                     x, y, w, h = (detection_data['left'][i],
#                                   detection_data['top'][i],
#                                   detection_data['width'][i],
#                                   detection_data['height'][i])

#                     if avg_x_left < x < eco_x_right:
#                         detected_letters.append(letter)

#             # plt.figure(figsize=(12, 6))

#             # plt.subplot(1, 2, 1)
#             # plt.title(f'Lower Middle Region with Detected Words - {filename}')
#             # plt.imshow(cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2RGB))
#             # plt.axis('off')

#             # plt.subplot(1, 2, 2)
#             # plt.title('Binary Image')
#             # plt.imshow(binary, cmap='gray')
#             # plt.axis('off')

#             # plt.show()

#             print("Detected Words:", words)
#             print("Detected Letters within the boundaries of 'average' and 'economy':", detected_letters)
#         else:
#             print(f"One or both words not found in image: {filename}.")
