import os

from fuel_economy import get_fuel_economy
from small_symbols_detection import get_small_symbol_information
from analog_detecter import get_analog_output
from middle_information import get_middle_information

if __name__ == '__main__':
    image_directory = os.path.join(os.getcwd(),'Images')
    analog_output_folder = os.path.join(os.getcwd(),'Analog_output')

    for images in os.listdir(image_directory):
        print(f"For the image {os.path.join(image_directory,images)}")
        image_path = os.path.join(image_directory,images)
        get_fuel_economy(image_path)
        get_small_symbol_information(image_path)
        print('\n')
        get_analog_output(image_path,analog_output_folder,images)
        get_middle_information(image_path)
