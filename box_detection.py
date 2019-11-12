import cv2
import numpy as np
import os

def box_extraction(img_for_box_extraction_path, cropped_dir_path, img_name):

    color_img = cv2.imread(img_for_box_extraction_path)
    img = cv2.imread(img_for_box_extraction_path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255,
                                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    #cv2.imwrite("Image_bin.jpg", img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//40

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, kernel_length))

    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    #cv2.imwrite("verticle_lines.jpg", verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    # cv2.imwrite("horizontal_lines.jpg", horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(
        verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(
        img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Invert the image again, because find countours only works on white objects
    img_final_bin = 255-img_final_bin

    # For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    resized_img = cv2.resize(img_final_bin, (960, 720))
    cv2.imshow("img_final_bin.jpg", resized_img) 
    cv2.waitKey(0)
    #cv2.imwrite("img_final_bin.jpg", img_final_bin)

    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(
        img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom. Need to actually make sort_contours or some issue with importing function
    # (contours, boundingBoxes) = sort_contours(
    #     contours, method="top-to-bottom")

    idx = 0
    for item in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(item)

        # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
        if (w > 300 and h > 300 and w/h > 0.86 and w/h < 1.25):
            idx += 1
            new_img = color_img[y:y+h, x:x+w]
            cv2.imwrite(cropped_dir_path+r"\\"+img_name+r"_cropped_" +
                        str(idx) + '.jpg', new_img)  
    
    # Debugging
    # resized_img = cv2.resize(color_img, (960, 720))
    # cv2.imshow("color image", resized_img) 
    # cv2.waitKey(0)

    # Draws contours only on good contours, can't move this to first for loop because draws lines over the image
    box_num = 0
    areas = []
    temp_img_drawn = color_img
    for index, item in enumerate(contours):
        area = cv2.contourArea(item)
        if(area>138000 and area <200000): # Problem need to reorient images with Hough lines
            cv2.drawContours(temp_img_drawn, contours, index, (0,255,0), 3)
            box_num +=1
            areas.append(area)

    # See the countours drawn over image
    #cv2.imwrite(cropped_dir_path+r"\\" + "drawn_img.jpg", drawn_img)
    print(img_name + ' ', areas)
    resized_img = cv2.resize(temp_img_drawn, (960, 720))
    cv2.imshow(str(img_name) + " Drawn over image boxes counted: " + str(box_num), resized_img) 
    cv2.waitKey(0)

# Single image box detection
box_extraction(r"4x4 hemo grid slanted after 4 hours.jpg", r"Hemo_images\cropped", 'image_11')

# Loop through files in a directory 
# rootdir = r'Hemo_images\images_to_crop'
# destination = r'Hemo_images\cropped'
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         temp_name = os.path.join(subdir, file)
#         box_extraction(temp_name, destination,file[:-4])
        