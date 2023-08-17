import numpy as np

from .interpolation import interpolation
from dip import *
import math


class Distort:
    def __init__(self):
        pass

    def distortion(self, image, k):
        """Applies distortion to the image
                image: input image
                k: distortion Parameter
                return the distorted image"""

        distorted_image = zeros(image.shape, uint8)
        rows = image.shape[0]
        cols = image.shape[1]
        centerX = rows // 2
        centerY = cols // 2

        for x in range(rows):
            for y in range(cols):
                [xc, yc] = [x - centerX, y - centerY]

                d = math.sqrt(xc ** 2 + yc ** 2)
                const = 1 / (1 + (k * d))

                [xcd, ycd] = [round(const * xc), round(const * yc)]

                [xd, yd] = [xcd + centerX, ycd + centerY]

                distorted_image[xd, yd] = image[x, y]

        return distorted_image

    def correction_naive(self, distorted_image, k):

        correctedImage = zeros(distorted_image.shape, uint8)

        rows = distorted_image.shape[0]
        cols = distorted_image.shape[1]
        centerX = rows // 2
        centerY = cols // 2

        for x in range(rows):
            for y in range(cols):
                [xcd, ycd] = [x - centerX, y - centerY]

                d = math.sqrt(xcd ** 2 + ycd ** 2)

                const = (1 + k * d)

                [xc, yc] = [round(const * xcd), round(const * ycd)]

                [xo, yo] = [xc + centerX, yc + centerY]
                i = xc + centerX
                j = yc + centerY

                if i < rows and j < cols and i >= 0 and j >= 0:
                    correctedImage[xo, yo] = distorted_image[x, y]

        return correctedImage

    def correction(self, distorted_image, k, interpolation_type):

        corrected = zeros(distorted_image.shape, uint8)

        rows = distorted_image.shape[0]
        cols = distorted_image.shape[1]
        centerX = rows // 2
        centerY = cols // 2

        for x in range(rows):
            for y in range(cols):
                [xc, yc] = [x - centerX, y - centerY]

                d = math.sqrt(xc ** 2 + yc ** 2)
                const = 1 / (1 + (k * d))

                [xcd, ycd] = [const * xc, const * yc]

                xd = xcd + centerX
                yd = ycd + centerY
                pt = (xd, yd)

                if interpolation_type == "bilinear":

                    Q11 = (math.floor(xd), math.floor(yd))
                    Q12 = (math.floor(xd), math.ceil(yd))
                    Q21 = (math.ceil(xd), math.floor(yd))
                    Q22 = (math.ceil(xd), math.ceil(yd))
                    neighbors = [Q11, Q12, Q21, Q22]
                    values = []
                    for point in neighbors:
                        values.append(distorted_image[point[0], point[1]])

                    importHolder = interpolation()
                    biLinVal = importHolder.bilinear_interpolation(neighbors,values, pt)

                    corrected[x, y] = biLinVal


                else:
                    xNN = round(xd)
                    yNN = round(yd)
                    corrected[x, y] = distorted_image[xNN, yNN]

        return corrected
