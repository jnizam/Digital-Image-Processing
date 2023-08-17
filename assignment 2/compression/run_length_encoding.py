from dip import *
from dip import ones, array

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        code = []
        rows = binary_image.shape[0]
        cols = binary_image.shape[1]

        count = 0

        for r in range(rows):
            ref = binary_image[r][0]
            code.append(str(ref))
            for c in range(cols):
                if binary_image[r][c] == ref:
                    count += 1
                else:
                    ref = binary_image[r][c]
                    code.append(count)
                    count = 1
            code.append(count)
            count = 0
    
        return code

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        image = []
        curr = 0
        for val in rle_code:
            if val == '0':
                curr = 0
            elif val == '255':
                curr = 1
            elif curr == 0:
                temp = zeros(val, dtype=int)
                image.extend(temp)
                curr = 1
            else:
                temp = ones(val, dtype=int) * 255
                image.extend(temp)
                curr = 0
        decodedImage = array(image).reshape(height,width)

        return decodedImage





        




