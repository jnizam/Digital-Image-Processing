import math
from dip import *
"""
Do not import cv2, numpy and other third party libs
"""


class Operation:

    def __init__(self):
        pass

    def merge(self, image_left, image_right, column):
        """
        Merge image_left and image_right at column (column)
        
        image_left: the input image 1
        image_right: the input image 2
        column: column at which the images should be merged

        returns the merged image at column
        """
        # new code
        merged_image = zeros(image_left.shape, uint8)
        rows = merged_image.shape[0]
        cols = merged_image.shape[1]

        for x in range(rows):
            for y in range(cols):
                if y < column:
                    merged_image[x, y] = image_left[x, y]
                else:
                    merged_image[x, y] = image_right[x, y]



        # Please do not change the structure
        return merged_image  # Currently the original image is returned, please replace this with the merged image

    def color_slicing(self, color_image, blackwhite_image, target_color, threshold):
        """
        Perform color slicing to create an image where only the targeted color is preserved and the rest
        is black and white

        color_image: the input color image
        blackwhite_image: the input black and white image
        target_color: the target color to be extracted
        threshold: the threshold to determine the pixel to determine the proximity to the target color

        return: output_image
        """
        
        # add your code here
        outputImage = zeros(color_image.shape, uint8)
        rows = outputImage.shape[0]
        cols = outputImage.shape[1]

        for x in range(rows):
            for y in range(cols):
                dist = math.sqrt(sum((color_image[x, y, :] - target_color) ** 2))
                if dist <= threshold:
                    outputImage[x, y] = color_image[x, y]
                else:
                    outputImage[x, y] = blackwhite_image[x, y]


        # final = gray_image * mask_in


        # Please do not change the structure
        return outputImage  # Currently the input image is returned, please replace this with the color extracted image

   