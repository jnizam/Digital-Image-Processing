import dip
from dip import zeros, putText, FONT_HERSHEY_SIMPLEX, LINE_AA

class ShapeCounting:
    def __init__(self):
        pass
    
    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes as input:
        image: binary image
        return: a list/dict of regions
        """
        
        regions = dict()
        rows = image.shape[0]
        cols = image.shape[1]

        R = zeros((rows,cols),dtype=int)
        count = 0

        for i in range(rows):
            for j in range(cols):
                if image[i][j] == 255:
                    #edge case for first pixel
                    if i == 0 and j == 0:
                        count += 1
                        R[i][j] = count
                        regions[R[i][j]] = []
                        regions[R[i][j]].append((i,j))
                    #edge case for first row
                    elif i == 0:
                        left = R[i][j-1]
                        if left == 0:
                            count += 1
                            R[i][j] = count
                            regions[R[i][j]] = []
                            regions[R[i][j]].append((i,j))
                        else:
                            R[i][j] = left
                            regions[left].append((i,j))
                    #edge case for first column
                    elif j == 0:
                        top = R[i-1][j]
                        if top == 0:
                            count += 1
                            R[i][j] = count
                            regions[R[i][j]] = []
                            regions[R[i][j]].append((i,j))
                        else:
                            R[i][j] = top
                            regions[top].append((i,j))
                    #general case
                    else:
                        top = R[i-1][j]
                        left = R[i][j-1]
                        if top == 0 and left == 0:
                            count += 1
                            R[i][j] = count
                            regions[R[i][j]] = []
                            regions[R[i][j]].append((i,j))
                        elif (top == 0 and left != 0) or (top != 0 and left != 0 and top == left):
                            R[i][j] = left
                            regions[left].append((i,j))
                        elif top != 0 and left == 0:
                            R[i][j] = top
                            regions[top].append((i,j))
                        else:
                            R[i][j] = top
                            R[i][j-1] = top

                            regions[top].append((i,j))
                            regions[top].extend(regions[left])
                            regions[left].clear()
        
        #removes the noise (anything less than 10 pixels)
        for i in range(count):
            if len(regions[i+1]) < 10:
                regions.pop(i+1)

        return regions

    def identify_shapes(self, region):
        """Compute shape features area and centroid, and shape
        Ignore shapes smaller than 10 pixels in area.
        takes as input
        region: a list/dict of pixels in a region
        returns: shapes, a data structure with centroid, area, and shape (c, s, r, or e) for each region
        c - circle, s - squares, r - rectangle, and e - ellipse
        """

        # Please print your shape statistics to stdout, one line for each shape
        # Region: <region_no>, centroid: <centroid>, area: <shape area>, shape: <shape type>
        # Example: Region: 871, centroid: (969.11, 51.11), area: 707, shape: c

        regionNum = 0
        shapes = {}
        for keys,value in list(region.items()):
            stats = {}
            regionNum += 1

            #area
            area = len(value)
            stats['area'] = area

            #find centroid
            sumX, sumY = 0, 0
            for i in range(area):
                sumX += value[i][0]
                sumY += value[i][1]
            centerX = int(sumX/area)
            centerY = int(sumY/area)
            centroid = (centerX, centerY)

            stats['center'] = centroid

        #find shape
            #finding min and max values relative to the centroid axes.
            left = min([point for point in value if point[1] == centerY], key=lambda point: point[0])
            right = max([point for point in value if point[1] == centerY], key=lambda point: point[0])

            up = max([point for point in value if point[0] == centerX], key=lambda point:point[1])
            down = min([point for point in value if point[0] == centerX], key=lambda point:point[1])

            distHorizontal = right[0] - left[0]
            distVertical = up[1] - down[1]
        #had a 15% margin of error for area similarity as it gave best accuracy
            #either square or circle
            if distHorizontal == distVertical:
                if 0.85 * area <= distHorizontal*distVertical <= 1.15 * area:
                    stats['shape'] = 's'
                else:
                    stats['shape'] = 'c'
            #either ellipses or rectangle
            else:
                if 0.85 * area <= distHorizontal*distVertical <= 1.15 * area:
                    stats['shape'] = 'r'
                else:
                    stats['shape'] = 'e'

            shapes[regionNum] = stats
        
        return shapes

    def count_shapes(self, shapes_data):
        """Compute the count of shapes using the shapes data returned from identify shapes function
           takes as input
           shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
           returns: a dictionary with count of each shape
           Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
           """
        
        counts = {}
        square = 0
        rectangle = 0
        circle = 0
        ellipse = 0

        for keys,value in list(shapes_data.items()):
            Myshape = value['shape']

            if Myshape == 'c':
                circle += 1
            elif Myshape == 's':
                square += 1
            elif Myshape == 'e':
                ellipse += 1
            else:
                rectangle += 1

        counts['circles'] = circle
        counts['ellipses'] = ellipse
        counts['rectangles'] = rectangle
        counts['squares'] = square

        return counts

    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""

        withText = image.copy()

        
        for keys,value in list(shapes_data.items()):
            center = (value['center'][1], value['center'][0])
            if value['shape'] == 'c':
                putText(withText, 'c', center, FONT_HERSHEY_SIMPLEX, 1, 2, 2, LINE_AA, bottomLeftOrigin=False)
            elif value['shape'] == 's':
                putText(withText, 's', center, FONT_HERSHEY_SIMPLEX, 1, 2, 2, LINE_AA, bottomLeftOrigin=False)
            elif value['shape'] == 'e':
                putText(withText, 'e', center, FONT_HERSHEY_SIMPLEX, 1, 2, 2, LINE_AA, bottomLeftOrigin=False)
            else:
                putText(withText, 'r', center, FONT_HERSHEY_SIMPLEX, 1, 2, 2, LINE_AA, bottomLeftOrigin=False)  
    
        return withText

