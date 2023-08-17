from dip import zeros
import math


class Filtering:

    def __init__(self, image):
        self.image = image
        # add padding
         

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""
        filter = zeros((5,5))
        sum = 0
        for i in range(5):
            for j in range(5):
                x,y  = i - 2, j - 2
                exp = (-1*(x**2 + y**2))/2
                eval = math.exp(exp)
                G = (1/(2*math.pi)) * eval
                sum += G
                filter[i][j] = G
        return filter, sum

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""
        #using the [-8 & 1]filter
        filter = zeros((3,3))
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    filter[i][j] = -8
                else:
                    filter[i][j] = 1

        return filter

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """
        if filter_name == 'gaussian':
            filter, sum = self.get_gaussian_filter()
            #pad image
            paddedImg = zeros((self.image.shape[0] + 4, self.image.shape[1] + 4))
            paddedImg[2:-2,2:-2] = self.image

            #apply filter
            output = zeros(paddedImg.shape)

            for i in range(2, paddedImg.shape[0] - 2):
                for j in range(2, paddedImg.shape[1] - 2):
                    
                    val = 0
                    subimage = paddedImg[i-2:i+3, j-2:j+3]
                    for x in range(subimage.shape[0]):
                        for y in range(subimage.shape[1]):
                            val += subimage[x][y] * filter[x][y]
                    val = val / sum

                    output[i][j] = val
                    
            return output[2:-2, 2:-2] # remove padding
        
        else:
            filter = self.get_laplacian_filter()
            #pad image
            paddedImg = zeros((self.image.shape[0] + 2, self.image.shape[1] + 2))
            paddedImg[1:-1,1:-1] = self.image

            #apply filter
            output = zeros(paddedImg.shape)
            for i in range(1, paddedImg.shape[0] - 1):
                for j in range(1, paddedImg.shape[1] - 1):
                    val = 0

                    subimage = paddedImg[i-1:i+2, j-1:j+2]
                    for x in range(subimage.shape[0]):
                        for y in range(subimage.shape[1]):
                            val += subimage[x][y] * filter[x][y]
                    val = val

                    output[i][j] = val

            return output[1:-1, 1:-1] #remove padding

