import cv2
import numpy as np
import math
import os

def zoom_and_save(image_path, output_path, zoom_ratio):
    """
    Zooms an image by a given ratio and saves the zoomed image.

    Parameters:
        image_path (str): Path to the input image.
        output_path (str): Path to save the zoomed image.
        zoom_ratio (float): The zoom factor. Values > 1 zoom in, values < 1 zoom out.

    Returns:
        None
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")

    # Calculate the new dimensions
    new_width = int(image.shape[1] * zoom_ratio)
    new_height = int(image.shape[0] * zoom_ratio)

    # Resize the image
    zoomed_img = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # If the zoomed image is larger, crop it to match the original dimensions
    if zoom_ratio > 1:
        x_start = (zoomed_img.shape[1] - image.shape[1]) // 2
        y_start = (zoomed_img.shape[0] - image.shape[0]) // 2
        zoomed_img = zoomed_img[y_start:y_start + image.shape[0], x_start:x_start + image.shape[1]]

    # If the zoomed image is smaller, pad it to match the original dimensions
    elif zoom_ratio < 1:
        pad_x = (image.shape[1] - zoomed_img.shape[1]) // 2
        pad_y = (image.shape[0] - zoomed_img.shape[0]) // 2
        zoomed_img = cv2.copyMakeBorder(zoomed_img, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    # Save the zoomed image
    cv2.imwrite(output_path, zoomed_img)
    print(f"Zoomed image saved at: {output_path}")




# Function to detect the circle and the needle, calculate the angle
def get_circle_center(image):
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

        return x,y

    return None, None

def calculate_circle_ratio(img, output_path=None):
    """
    Calculates the ratio of the line joining the centers of the left and right circles
    to the length (width) of the image. Marks the detected circles and the connecting line
    on the image and saves the marked image if an output path is provided.
    # """

    width = img.shape[1]
    length = img.shape[0]
    # print(f"{width} {length} {width/length}")
    img_left = img[:, :width//2]
    img_right = img[:, width//2:]
    xl,yl =  get_circle_center(img_left)
    xr,yr = get_circle_center(img_right)

    if xl is None or xr is None:
       return -1

    center_distance = math.sqrt((xl - xr) ** 2 + (yl - yr) ** 2)

    return (width+length)/center_distance


def ratio_calculator(image_path):
    """
    Wrapper function to calculate the ratio for an image and save the marked image.
    """
    image = cv2.imread(image_path)

    ratio = calculate_circle_ratio(image)
    if(ratio!=-1):
        print(f"The ratio for {image_path} is {ratio}")
    else:
        print(f"Circle cannot be detected")
    return ratio

def zoom_image(zoom_factor, input_image_path, output_folder,image_name):

    output_image_path = os.path.join(output_folder,file)
    zoom_and_save(input_image_path, output_image_path, zoom_factor)

input_folder = "./new_images"

if not os.path.exists(os.path.join(os.getcwd(),'./new_images2')):
    os.makedirs(os.path.join(os.getcwd(),'./new_images2'))


ideal_ratio = ratio_calculator(os.path.join(os.path.join(os.getcwd(),'Images'),'6.jpg'))


for file in os.listdir(input_folder):
    image_path = os.path.join(input_folder, file)
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check valid image extensions
        zoom_factor= ratio_calculator(image_path)/ideal_ratio
        print(ratio_calculator(image_path))
        print(f"Zoom factor for {file} is {zoom_factor}")
        if(zoom_factor>=1):
            print("Cropped")
            zoom_image(zoom_factor,image_path,os.path.join(os.getcwd(),'new_images2'),file)






