from manim import*
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from matplotlib.colors import LinearSegmentedColormap

class ThreeDPlot(Scene):
    def construct(self):
        img = Image.open("cropped1_image.jpg")  
        img = img.resize((10, 10)) 
        image_matrix = np.array(img)

        grid = VGroup()
        number_of_cols = len(image_matrix[0])
        number_of_rows = len(image_matrix)
        square_size = 0.5  
        squares1 = Group()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                squares1.add(square)
                square.move_to((j * square_size, -i * square_size, 0))  # Vị trí của mỗi ô vuông
                number = Text(str(image_matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid.add(VGroup(square, number))
        
        self.add(grid)
        self.wait(3)