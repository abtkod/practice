import unittest

def rotate_matrix(image, is_clockwise):    
    N = len(image[0])
    for i in range(N//2):    	
        for j in range(i, N-i-1):
            if is_clockwise:
                temp = image[i][j]
                image[i][j] = image[-j-1][i]
                image[-j-1][i] = image[-i-1][-j-1]
                image[-i-1][-j-1] = image[j][-i-1]
                image[j][-i-1] = temp
            else:
                pass
                # is done similarly

class Pixel:
    def __init__(self, G, B, R, H):
        self.G, self.B, self.R, self.H = G, B, R, H
    def __repr__(self):
        return str((self.G, self.B, self.R, self.H))


class Test(unittest.TestCase):
    image = [[Pixel(0,0,0,0), Pixel(0,1,0,1)], [Pixel(1,0,1,0), Pixel(1,1,1,1)]]
    rotated = [[Pixel(1,0,1,0), Pixel(0, 0, 0, 0)], [Pixel(1, 1, 1, 1), Pixel(0, 1, 0, 1)]]

    # image = [[x for x in range(i*5, (i+1)*5)] for i in range(5)]
    # rotated = [[x-5*i for i in range(5)] for x in range(20, 25)]

    
    def test_rotation(self):        
        rotate_matrix(self.image, True)                
        self.assertEqual(repr(self.rotated), repr(self.image))

if __name__ == "__main__":
    unittest.main()