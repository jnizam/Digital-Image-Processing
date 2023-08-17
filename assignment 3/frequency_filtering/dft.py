# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
from dip import zeros
import math

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""

        DFT = zeros((15,15), dtype=complex)
        for u in range(15):
            for v in range(15):
                F = 0
                for i in range(15):
                    for j in range(15):
                        F += matrix[i][j] * (math.cos((2*math.pi/15) * ((u * i) + (v * j))) 
                                            - 1j * math.sin((2*math.pi/15) * ((u * i) + (v * j))))
                DFT[u][v] = F 
        return DFT

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""
        
        inverse = zeros((15,15), dtype=complex)

        for i in range(15):
            for j in range(15):
                I = 0
                for u in range(15):
                    for v in range(15):
                        I += matrix[u][v] * (math.cos((2*math.pi/15) * ((u * i) + (v * j))) 
                                            + 1j * math.sin((2*math.pi/15) * ((u * i) + (v * j))))
                inverse[i][j] = I / 15**2
        
        return inverse

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""

        mag = zeros((15,15), dtype=int)
        for i in range(15):
            for j in range(15):
                real = matrix[i][j].real
                img = matrix[i][j].imag

                dist = math.sqrt(real**2 + img**2)
                mag[i][j] = round(dist)
    
       
        return mag