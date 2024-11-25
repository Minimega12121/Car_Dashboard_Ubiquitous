import cv2
import numpy as np
import os

# Create output directory if it doesn't exist
output_path = "images_marked/"
os.makedirs(output_path, exist_ok=True)

# Specify the path to your images
path = "Images/"

for files in os.listdir(path):
    image_path = os.path.join(path, files)

    # Load the image
    image = cv2.imread(image_path)

    # If the image can't be loaded, skip to the next one
    if image is None:
        print(f"Image {image_path} not found or cannot be opened.")
        continue

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Define regions of interest (ROI) for brake, seatbelt, left indicator, right indicator, fog light, and parking lights
    roi_brake = (int(0.55 * width), int(0.05 * height), int(0.15 * width), int(0.28 * height))  # Upper-right for brake
    roi_seatbelt = (int(0.08 * width), int(0.46 * height), int(0.115 * width), int(0.15 * height))  # Middle-left for seatbelt
    roi_left_indicator = (int(0.3 * width), int(0.1 * height), int(0.2 * width), int(0.25 * height))  # Upper-left for left indicator
    roi_right_indicator = (int(0.6 * width), int(0.1 * height), int(0.2 * width), int(0.25 * height))  # Upper-right for right indicator

    # New ROI for fog light (you can adjust these values as per your requirement)
    roi_fog_light = (int(0.21 * width), int(0.38 * height), int(0.07 * width), int(0.15 * height))  # Bottom-center for fog light

    # New ROI for parking lights (you can adjust these values as per your requirement)
    roi_parking_lights = (int(0.26 * width), int(0.44 * height), int(0.07 * width), int(0.15* height))  # Bottom-center for parking lights

    # Draw rectangles for each ROI
    # Brake indicator
    x_brake, y_brake, w_brake, h_brake = roi_brake
    cv2.rectangle(image, (x_brake, y_brake), (x_brake + w_brake, y_brake + h_brake), (0, 255, 0), 2)  # Green color for brake

    # Seatbelt indicator
    x_seatbelt, y_seatbelt, w_seatbelt, h_seatbelt = roi_seatbelt
    cv2.rectangle(image, (x_seatbelt, y_seatbelt), (x_seatbelt + w_seatbelt, y_seatbelt + h_seatbelt), (0, 0, 255), 2)  # Red color for seatbelt

    # Left indicator
    x_left_indicator, y_left_indicator, w_left_indicator, h_left_indicator = roi_left_indicator
    cv2.rectangle(image, (x_left_indicator, y_left_indicator), (x_left_indicator + w_left_indicator, y_left_indicator + h_left_indicator), (255, 0, 0), 2)  # Blue color for left indicator

    # Right indicator
    x_right_indicator, y_right_indicator, w_right_indicator, h_right_indicator = roi_right_indicator
    cv2.rectangle(image, (x_right_indicator, y_right_indicator), (x_right_indicator + w_right_indicator, y_right_indicator + h_right_indicator), (255, 255, 0), 2)  # Yellow color for right indicator

    # Fog light
    x_fog, y_fog, w_fog, h_fog = roi_fog_light
    cv2.rectangle(image, (x_fog, y_fog), (x_fog + w_fog, y_fog + h_fog), (0, 255, 0), 2)  # Green color for fog light

    # Parking lights
    x_parking, y_parking, w_parking, h_parking = roi_parking_lights
    cv2.rectangle(image, (x_parking, y_parking), (x_parking + w_parking, y_parking + h_parking), (0, 255, 0), 2)  # Green color for parking lights

    # Save the marked image in the output directory
    marked_image_path = os.path.join(output_path, files)
    cv2.imwrite(marked_image_path, image)

print("Marked images have been saved in the 'images_marked/' directory.")
