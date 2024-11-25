import cv2
import numpy as np
import pytesseract
import os
from matplotlib import pyplot as plt

def process_image(image_path, output_path):
    print(f'Processing image: {os.path.basename(image_path)}')

    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    height, width = image.shape[:2]
    lower_middle_y_start = int(height * 0.7)
    lower_middle_y_end = height
    lower_middle_x_start = int(width * 0.42)
    lower_middle_x_end = int(width * 0.55)

    lower_middle_region = image[lower_middle_y_start:lower_middle_y_end, lower_middle_x_start:lower_middle_x_end]

    gray = cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    blurred = cv2.GaussianBlur(denoised, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_symbols = []
    target_symbols = {'L', 'P', 'D', 'N', 'R'}

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if 30 < w < 500 and 30 < h < 700 and (0.01 < w/h < 4):
            symbol_region = morph[y:y + h, x:x + w]

            symbol_text = pytesseract.image_to_string(symbol_region, config='--psm 10 -c tessedit_char_whitelist=LPRDN').strip().upper()

            if symbol_text in target_symbols:
                detected_symbols.append(symbol_text)
                cv2.rectangle(lower_middle_region, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(lower_middle_region, symbol_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                print(f"Detected '{symbol_text}' at position (x: {x}, y: {y}), size (w: {w}, h: {h})")
                print(f"ROI for text detection: (x: {x}, y: {y}, width: {w}, height: {h})")

    marked_image_path = os.path.join(output_path, "marked_" + os.path.basename(image_path))
    cv2.imwrite(marked_image_path, lower_middle_region)

    if detected_symbols:
        print(f"Image: {os.path.basename(image_path)} - Detected driving modes: {detected_symbols}")
    else:
        print(f"Image: {os.path.basename(image_path)} - No driving mode detected")

    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(lower_middle_region, cv2.COLOR_BGR2RGB))
    plt.title(f'Detected Driving Modes - {os.path.basename(image_path)}')
    plt.axis('off')
    plt.show()

output_path = "images_marked_with_symbols/"
os.makedirs(output_path, exist_ok=True)

images_path = "./Images/"

for filename in os.listdir(images_path):
    if filename != '3.jpg': continue
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(images_path, filename)
        process_image(image_path, output_path)

print("Images with detected symbols have been saved in 'images_marked_with_symbols/' directory.")
