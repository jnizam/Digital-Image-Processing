from dip import *
import math
import numpy as np
class Coloring:

    def intensity_slicing(self, image, n_slices):
        '''
       Convert greyscale image to color image using color slicing technique.
       takes as input:
       image: the grayscale input image
       n_slices: number of slices
        
       Steps:
 
        1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
        2. Randomly assign a color to each interval
        3. Create and output color image
        4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
 
       returns colored image
       '''
        colored = zeros((image.shape[0], image.shape[1], 3), dtype = uint8)

        numIntervals = n_slices + 1
        intervals = arange(0,256,255/(numIntervals))
        intervals = intervals.astype(int)

        colors = []
        for i in range(numIntervals):
            c = (random.randint(0,256), random.randint(0,256), random.randint(0,256))
            colors.append(c)

        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                for i in range(1, len(intervals)):
                    if image[x,y] < intervals[i]:
                        colored[x,y] = colors[i - 1]
                        break

        return colored
    
    def color_transformation(self, image, n_slices, theta):
        '''
        Convert greyscale image to color image using color transformation technique.
        takes as input:
        image:  grayscale input image
        colors: color array containing RGB values
        theta: (phase_red, phase,_green, phase_blue) a tuple with phase values for (r, g, b) 
        Steps:
  
         1. Split the exising dynamic range (0, k-1) using n slices (creates n+1 intervals)
         2. create red values for each slice using 255*sin(slice + theta[0])
            similarly create green and blue using 255*sin(slice + theta[1]), 255*sin(slice + theta[2])
         3. Create and output color image
         4. Iterate through the image and assign colors to the color image based on which interval the intensity belongs to
  
        returns colored image
        '''
        

        colored = zeros((image.shape[0], image.shape[1], 3), dtype = uint8)
        
        intervals = []

        for x in range(n_slices + 1):
            intervals.append(x * (255//n_slices))
        intervals.append(255)


        colors = []
        for i in range(1, len(intervals)):
            mid = (((intervals[i]) + (intervals[i - 1] + 1)) / 2)
            c = (int(255 * (abs(math.sin(mid + theta[0])))), int(255 * (abs(math.sin(mid + theta[1])))), int(255 * (abs(math.sin(mid + theta[2])))))
            colors.append(c)

        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                for i in range(len(colors)):
                    if image[x,y] <= intervals[i + 1]:
                        colored[x,y] = colors[i]
                        break

        return colored
    

    
     




        

