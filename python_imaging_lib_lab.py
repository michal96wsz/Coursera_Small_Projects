import PIL.Image as img
import os, sys, math
from concurrent.futures import ThreadPoolExecutor
def check_images_format(expected_image_format: str, images_dir_path=None):
    image_files_to_be_converted_list = []


    if images_dir_path is None:
        images_dir_path = os.getcwd()
    else:
        if os.path.exists(images_dir_path):
            pass
        else:
            images_dir_path = input("Provided images path does not exist, please provide valid path:")

    try:
        image_extensions_list = ["jpeg", "gif", "png", "tiff", "bmp"]

        try:
            image_extensions_list.remove(expected_image_format)
        except ValueError as e:
            print(e, f"\n expected images format {expected_image_format} is not in the list of most common ones ")
            print(f"Are you sure you want to convert all files with extension of: {image_extensions_list} to {expected_image_format}?")
            proceed_decision = input("y -> yes, n -> no")
            if proceed_decision.lower() != "y":
                sys.exit(3)

        image_extensions_tuple = tuple(image_extensions_list)
        for path, dirs, files in os.walk(images_dir_path):
            for file in files:
                print(file)
                if file.endswith(image_extensions_tuple):
                    image_files_to_be_converted_list.append(os.path.join(path, file))


                    #Ok tutaj trzeba sobie przekonwertowac pliki i chyba nic szczegolnego to nie wymaga, zwykle copy paste
                    #ale pojawia sie pytanie, czy nie lepiej zebrac sobie liste plikow ktore maja byc skopiowane
                    #a nastepnie sobie z jakims multi-threadingiem to pocisnac?

        return image_files_to_be_converted_list

    except OSError as e:
        print("Provided path is still not valid! ", e)
        exit(4)


def perform_rotation_and_conversion(convert_rotate_file_path: str, file_format: str, file_destination=None):

    if file_destination is None:
        file_destination = os.path.join(os.getcwd(), "Processed_Images")


    if not os.path.exists(file_destination):
        try:
            os.mkdir(file_destination)
        except OSError as e:
            print("There is a problem with images destination! ", e)

    print(os.path.join(file_destination, os.path.basename(convert_rotate_file_path)))
    image_file = img.open(convert_rotate_file_path)
    rotated_image_file = image_file.rotate(90.0, expand=True)
    rgb_rotated_image_file = rotated_image_file.convert("RGB")
    rgb_rotated_image_file.save(os.path.join(file_destination, os.path.basename(convert_rotate_file_path)), format=file_format)

    rgb_rotated_image_file.close()
    image_file.close()

def process_images(images_to_be_fully_processed_paths_list: list, final_format: str):

    images_count = len(images_to_be_fully_processed_paths_list)
    pool_workers_count = 0
    converting_threads_pool = None

    if images_count > 10:
        pool_workers_count = 10
    elif images_count == 0:
        print("No image file found under given path ", images_count)
        exit(5)
    else:
        pool_workers_count = math.ceil(images_count/2)

    # for image in images_to_be_fully_processed_paths_list:
    #     perform_rotation_and_conversion(image, final_format, None)
    #
    with ThreadPoolExecutor(max_workers=pool_workers_count) as executor:
        executor_results_list = []
        for image in images_to_be_fully_processed_paths_list:
            executor_results_list.append(executor.submit(perform_rotation_and_conversion, image, final_format, None))

        for executor_res in executor_results_list:
            executor_res.result()





if __name__ == "__main__":
    image_files_path = os.path.join(os.getcwd(), "obrazki")
    print(image_files_path)
    images_to_be_fully_processed_list = check_images_format("jpeg", image_files_path)
    process_images(images_to_be_fully_processed_list, "jpeg")
