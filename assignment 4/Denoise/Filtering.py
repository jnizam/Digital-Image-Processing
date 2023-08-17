from dip import *
import math
class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        
        """

        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        elif filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filter_size = filter_size
        
        # global_var: noise variance to be used in the Local noise reduction filter        
        self.global_var = var
        
        # S_max: Maximum allowed size of the window that is used in adaptive median filter
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""

        mean = 0
        for i in range (len(roi)):
            mean += roi[i]
        mean /= len(roi)
            

        
        return mean
    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        mean = 1
        for i in range(len(roi)):
            mean *= roi[i]
        mean = mean ** (1/len(roi))
        return mean

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        localMean = sum(roi) / len(roi)
        size = len(roi)

        localVal = 0

        for x in roi:
            localVal += (x - localMean)**2

        localVal /= size

        if localVal == 0:
            return localMean
        
        else:
            value = 0
            mid = size // 2
            mean = roi[mid] - localMean

            value = (1/localVal) * mean
            return value


    
    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi"""
        #sort
        roi = sorted(roi)

        median = 0
        if len(roi) % 2 == 0:
            median = roi[len(roi) / 2] + roi[(len(roi) / 2) - 1]
            median /= 2
        else:
            median = roi[int(len(roi) / 2)]
        return median

    
    def get_adaptive_median(self, pad_image, roi, windowSize, currRow, currCol):
        """Use this function to implment the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        minZ, maxZ = min(roi), max(roi)
        roi = sorted(roi)
        length = len(roi)
        mid = length // 2
        if length % 2 == 0:
            median = (roi[mid - 1] + roi[mid]) / 2
        else:
            median = roi[mid]
        medianZ = median
        var1 = medianZ - minZ
        var2 = medianZ - maxZ
        if var1 > 0 and var2 < 0:
            b1 = pad_image[currRow][currCol] - minZ
            b2 = pad_image[currRow][currCol] - maxZ
            if b1 > 0 and b2 < 0:
                return pad_image[currRow][currCol]
            else:
                return medianZ
        else:
            windowSize += 1
            if windowSize <= 15:
                updatedRoi = []
                padding = windowSize // 2
                for x in range(windowSize):
                    for y in range(windowSize):
                        updatedRoi.append(pad_image[currRow - padding + x][currCol - padding + y])
                return self.get_adaptive_median(pad_image, updatedRoi, windowSize, currRow, currCol)
            else:
                return medianZ
    
    

    def filtering(self):
        """performs filtering on an image containing gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernal and apply a mathematical
        operation for all the elements with in the kernel. For example, mean, median and etc.

        Steps:
        1. add the necesssary zero padding to the noisy image, that way we have sufficient values to perform the operati
        ons on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the ouput image.
        5. return the output image

        Note: You can create extra functions as needed. For example if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        
        if self.filter == self.get_local_noise:
            padding_size = self.filter_size // 2
            paddedImage = zeros((self.image.shape[0] + (2*padding_size), self.image.shape[1] + (2*padding_size)))
            paddedImage[padding_size:-padding_size, padding_size:-padding_size] = self.image

            outputImage = zeros((self.image.shape[0], self.image.shape[1]))
            mean = sum(self.image)/len(self.image)

            for i in range(padding_size, paddedImage.shape[0] - padding_size):
                for j in range(padding_size, paddedImage.shape[1] - padding_size):
                    roi = []
                    for x in range(self.filter_size):
                        for y in range(self.filter_size):
                            roi.append(paddedImage[i - padding_size + x][j - padding_size + y])
                    mean = self.filter(roi)
                    g_x_y = paddedImage[i][j]
                    mean = g_x_y - self.global_var * mean
                    outputImage[i - padding_size][j - padding_size] = mean

            return outputImage

        if self.filter == self.get_adaptive_median:
            padding_size = 15 // 2
            paddedImage = zeros((self.image.shape[0] + (2*padding_size), self.image.shape[1] + (2*padding_size)))
            for i in range(padding_size, paddedImage.shape[0] - padding_size):
                for j in range(padding_size, paddedImage.shape[1] - padding_size):
                    paddedImage[i][j] = self.image[i - padding_size][j - padding_size]

            windowSize = self.filter_size

            outputImage = zeros((self.image.shape[0], self.image.shape[1]))
            for i in range(padding_size, paddedImage.shape[0] - padding_size):
                for j in range(padding_size, paddedImage.shape[1] - padding_size):
                    z_xy = paddedImage[i][j]
                    roi = []
                    for x in range(windowSize):
                        for y in range(windowSize):
                            roi.append(paddedImage[i - windowSize + x][j - windowSize + y])
                    outputImage[i - padding_size][j - padding_size] = self.filter(paddedImage, roi, windowSize, i, j)

            return outputImage
        
        else:
            outputImage = zeros((self.image.shape[0], self.image.shape[1]))
            padding_size = self.filter_size//2
            paddedImage = zeros((self.image.shape[0] + (2*padding_size), self.image.shape[1] + (2*padding_size)))
            paddedImage[padding_size:-padding_size, padding_size:-padding_size] = self.image

            for i in range(padding_size, paddedImage.shape[0] - padding_size):
                for j in range(padding_size, paddedImage.shape[1] - padding_size):
                    roi = []
                    for x in range(self.filter_size):
                        for y in range(self.filter_size):
                            roi.append(paddedImage[i - padding_size + x][j - padding_size + y])
                    mean = self.filter(roi)
                    outputImage[i - padding_size][j - padding_size] = mean

            return outputImage

