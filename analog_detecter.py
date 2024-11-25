import cv2
import numpy as np
import os
import math

# Function to detect the circle and the needle, calculate the angle
def detect_circle_and_needle(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect circles using HoughCircles
    minRadius = int(blurred.shape[1] * 0.3)  # Adjust based on size
    maxRadius = int(blurred.shape[1] * 0.45)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        # Round to integer values for circle parameters
        circles = np.round(circles[0, :]).astype("int")
        x, y, r = circles[0]

        # Draw the detected circle and its center
        cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        cv2.circle(image, (x, y), 5, (0, 128, 255), -1)

        # Detect edges to find the needle
        edges = cv2.Canny(blurred, 50, 150)

        # Mask to isolate the region inside the circle
        mask = np.zeros_like(edges)
        cv2.circle(mask, (x, y), r, (255, 255, 255), thickness=-1)
        masked_edges = cv2.bitwise_and(edges, edges, mask=mask)

        # Use HoughLines to detect lines in the image
        lines = cv2.HoughLinesP(masked_edges, rho=1, theta=np.pi / 180, threshold=100,
                                minLineLength=int(r * 0.5), maxLineGap=10)

        if lines is not None:
            # Find the longest line (assumed to be the needle)
            max_length = 0
            needle_tip = None

            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

                # Check if the line starts near the circle center
                if length > max_length and (x1 - x) ** 2 + (y1 - y) ** 2 < r ** 2:
                    max_length = length
                    needle_tip = (x2, y2) if np.sqrt((x2 - x) ** 2 + (y2 - y) ** 2) > np.sqrt((x1 - x) ** 2 + (y1 - y) ** 2) else (x1, y1)

            if needle_tip is not None:
                # Draw a line from the center to the needle tip
                cv2.line(image, (x, y), needle_tip, (255, 0, 0), 2)

                # Calculate the angle between the needle and the right horizontal
                dx = needle_tip[0] - x
                dy = needle_tip[1] - y
                theta = math.degrees(math.atan2(dy, dx))

                # Normalize the angle to be in range [0, 360]
                if theta < 0:
                    theta += 360

                return image, (theta - 360) * -1

    return image, None

# Main function to process all images in the folder
def get_analog_output(img_path, output_folder, img_name):
    img = cv2.imread(img_path)

    # Crop the image to the left 50% (for the left-side analog)
    width = img.shape[1]
    img_left = img[:, :width//2]

    # Detect the circle and needle in the left side of the image
    processed_img_left, angle_left = detect_circle_and_needle(img_left)

    # Save the processed image with detected circle and needle for the left part
    output_path_left = os.path.join(output_folder, 'left_' + img_name)
    cv2.imwrite(output_path_left, processed_img_left)

    if angle_left is not None:
        print(f"{img_name} (Left) - Needle Angle: {angle_left:.2f} degrees")
        print(f"Analog Value: {7 -0.1- (angle_left) /30}")
    else:
        print(f"{img_name} (Left) - Circle or needle not detected.")


    # Crop the image to the right 50% (for the right-side speed analog)
    img_right = img[:, width//2:]

    # Detect the circle and needle in the right side of the image
    processed_img_right, angle_right = detect_circle_and_needle(img_right)

    # Save the processed image with detected circle and needle for the right part
    output_path_right = os.path.join(output_folder, 'right_' + img_name)
    cv2.imwrite(output_path_right, processed_img_right)

    if angle_right is not None:
        print(f"{img_name} (Right) - Needle Angle: {angle_right:.2f} degrees")
        print(f"Analog Value: {(9-(angle_right*10)/240-0.3)*20}kmph") # 3 units error
    else:
        print(f"{img_name} (Right) - Circle or needle not detected.")
