# Training data slicer: change tif to jpeg and then slice up large image into smaller tiles

import os
from PIL import Image
import image_slicer


# Converts tif to jpg and saves image; tif_img and jpeg_img are file names
def convert_tif_to_jpeg(tif_img, jpeg_img):

    image = Image.open(
        tif_img)
    image.convert(mode='RGB')
    image.save(jpeg_img)

    return


# Slices the image and saves each slice; jpeg_img is file name, num_slices is int number of slices, jpeg_slices is file name, slice_name is prefix for each slice
def slice_jpeg(jpeg_img, num_slices, jpeg_slices_folder, slice_name):

    tiles = image_slicer.slice(
        jpeg_img, num_slices, save=False)
    image_slicer.save_tiles(tiles, directory=jpeg_slices_folder,
                            prefix=slice_name, format='jpeg')

    return


# Converts all tif images in folder to jpeg slices in separate folder
def convert_tif_to_jpeg_slices(tif_image_list, tif_img_directory, jpeg_img_directory, jpeg_slices_directory, num_slices):

    for x in range(len(tif_image_list)):
        tif_img_directory = tif_img_directory + '\\' + str(tif_image_list[x])

        tempstr = str(tif_image_list[x])
        tempstr = tempstr.replace('tif', 'jpeg')
        jpeg_img_directory = jpeg_img_directory + '\\' + tempstr

        slice_name = str(tif_image_list[x])
        slice_name = slice_name.replace('.tif', '_slice')

        convert_tif_to_jpeg(tif_img_directory, jpeg_img_directory)
        slice_jpeg(jpeg_img_directory, num_slices,
                   jpeg_slices_directory, slice_name)

    return


# Creates a list of all the image file names in morpho_training folder
tif_image_list = os.listdir(
    r'G:\PyScripts\morpho_training\test_images\original')

print("All images in folder: ", tif_image_list)

# Variables
num_slices = 16  # 408x352 pixels, image_slicer automatically slices to possible number so odd number slices and unsliceable numbers get adjusted
# The r makes it a raw string otherwise you need to use double backslashes
tif_img_directory = r'G:\PyScripts\morpho_training\test_images\original'
jpeg_img_directory = r'G:\PyScripts\morpho_training\test_images\test_jpg'
jpeg_slices_directory = r'G:\PyScripts\morpho_training\test_images\test_slices'

convert_tif_to_jpeg_slices(tif_image_list, tif_img_directory,
                           jpeg_img_directory, jpeg_slices_directory, num_slices)
