class interpolation:

    def linear_interpolation(self, targetX, x1, x2, valuex1, valuex2):

        if x1 == x2:
            return valuex1
        else:
            I = (valuex1 * (x2 - targetX)) / (x2 - x1) + (valuex2 * (targetX - x1)) / (x2 - x1)
            return I

    def bilinear_interpolation(self, neighbors, values, point):
        i1 = self.linear_interpolation(point[0], neighbors[0][0], neighbors[2][0], values[0], values[2])
        i2 = self.linear_interpolation(point[0], neighbors[1][0], neighbors[3][0], values[1], values[3])
        finalI = self.linear_interpolation(point[1], neighbors[0][1], neighbors[1][1], i1, i2)

        return finalI
