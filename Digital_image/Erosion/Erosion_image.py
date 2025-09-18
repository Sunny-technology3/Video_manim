from manim import *
import cv2
import numpy
from PIL import Image
import operator
import matplotlib.pyplot as plt
from skimage import io

class ShowImage(Scene):
    def logo(self):
        image = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg")       
        '# Init logo start at mid of scene'
        image_cp = image.copy().scale(3)  
        # Set size and position of logo end
        image.scale(0.5).to_edge(UP).to_edge(LEFT).shift(LEFT * 0.4, UP * 0.4) 
        # Animate logo PTIT
        self.play(Succession( FadeIn(image_cp), Transform(image_cp, image)))        
        # Set position and attribute signature of team
        txt_intro = Text('''STDR2024 @EIC&DSP LAB\nDesigned by Le Minh Nam''',
                        font= "Segoe UI", font_size= 20
                        ).scale(2).move_to(ORIGIN)
        txt_intro.set_color(BLACK)
        self.play(Write(txt_intro), run_time = 1.5)
        self.play(txt_intro.animate.scale(0.3).to_edge(DR).shift(DOWN * 0.35, RIGHT * 0.35))
        txt_header = Text("Erosion in Image Processing", color = BLACK, font= "JetBrains Mono", font_size= 38).move_to(ORIGIN)
        self.play(Succession(Write(txt_header), ApplyWave(txt_header, scale_factor = 1.2), txt_header.animate.to_edge(UP).scale(0.8)))

    def construct(self):
        self.camera.background_color = WHITE
        self.logo()

        img = ImageMobject("example.jpg").scale(2)
        
        image = cv2.imread('example.jpg', 0)  # Đọc ảnh ở dạng grayscale (đen trắng)
        # Tạo kernel (hạt nhân) cho phép toán erosion
        kernel = np.ones((5,5), np.uint8)
        # Thực hiện phép toán erosion
        eroded_image = cv2.erode(image, kernel, iterations=1)
        cv2.imwrite("eroded_image.jpg", eroded_image)
        eroded_image1 = ImageMobject("eroded_image.jpg").scale(2).to_edge(RIGHT)
        self.play(FadeIn(img.move_to(ORIGIN)))
        self.wait(0.5)
        self.play(img.animate.move_to(LEFT*2))
        self.wait(1)

        red_overlay = Rectangle(width=2.5 * 0.1, height=2.5 * 0.1, color=RED, fill_opacity=0)
        # Tính toán vị trí của overlay trên ảnh gốc
        overlay_x = 12.5 * 0.1  # Tỉ lệ hóa theo kích thước của mỗi pixel (0.1 là kích thước mỗi pixel trên ảnh gốc trong Manim)
        overlay_y = 16 * 0.1  # Tỉ lệ hóa theo kích thước của mỗi pixel
        red_overlay.move_to(img.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        matrix = np.array([[0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 1, 1, 1, 1, 1, 1, 0],
                           [0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 0, 0, 0, 1, 1, 1, 1], 
                           [0, 0, 0, 0, 1, 1, 1, 1], 
                           [0, 1, 1, 1, 0, 0, 0, 1]])
        grid = VGroup()
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=BLACK, font="SF Pro", font_size=18).move_to(square.get_center())
                grid.add(VGroup(square, number))
        grid.move_to(img.get_corner(UL) + np.array([overlay_x, -overlay_y, 0])).scale(0.1)
        self.play(FadeIn(grid), grid.animate.scale(10).next_to(img, RIGHT * 2))
        s1 = Text("Input Matrix", font = "Segoe UI", color = BLACK, font_size= 25).next_to(grid, UP)
        self.play(Write(s1))
        self.play(Circumscribe(s1, color = BLUE, fade_out=True))
        self.wait(1)
        grid_text = Group(grid, s1)
        self.play(Succession(FadeOut(img, red_overlay), grid_text.animate.move_to(LEFT*4)))
        self.wait(0.5)

        #Structuring Element
        matrix1_check = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        matrix1 = np.array([[0, 1, 0], 
                            [1, 1, 1], 
                            [0, 1, 0]])
        grid1 = VGroup()
        number_of_cols1 = len(matrix1[0])
        number_of_rows1 = len(matrix1)
        for i in range(number_of_rows1):
            for j in range(number_of_cols1):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix1[i][j]), color=BLACK, font="SF Pro", font_size=18).move_to(square.get_center())
                grid1.add(VGroup(square, number))
        self.play(FadeIn(grid1.move_to(ORIGIN + DOWN*1.5)))
        s2 = Text("Structuring Element", font = "Segoe UI", color = BLACK, font_size= 20).next_to(grid1, UP)
        self.play(Write(s2))
        self.play(Succession(Circumscribe(s2, color = BLUE, fade_out=True), FadeOut(s2)))
        self.wait(0.5)

        #Eroded Matrix
        grid2 = Group() 
        square_group2 = Group()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                square_group2.add(square)
                grid2.add(square)
        self.play(FadeIn(grid2.next_to(grid, RIGHT*16)))
        s3 = Text("Eroded Matrix", font = "Segoe UI", color = BLACK, font_size= 25).next_to(grid2, UP)
        self.play(Write(s3))
        self.play(Circumscribe(s3, color = BLUE, fade_out=True))
        self.wait(0.5)

        for x in range(number_of_cols-3):
            for y in range(number_of_rows-1):
                square_group3 = VGroup()
                square_group_check = VGroup()
                grid_text_check = [[0 for _ in range(3)] for _ in range(3)]
                for i in range(x, x+3):
                    for j in range(y, y+3):
                        grid_text_check[i-x][j-y] = matrix[i][j]
                text_check1 = [grid_text_check[0][1], grid_text_check[1][0], grid_text_check[1][1], grid_text_check[1][2], grid_text_check[2][1]]
                for i in range(3):
                    for j in range(3):
                        square_group3.add(grid[(x+i)*number_of_cols + (j+y)][0])
                        square_group_check.add(grid[(x+i)*number_of_cols + (j+y)])
                square_group_check_copy = VGroup(*[obj.copy() for obj in square_group_check])
                self.play(square_group3.animate.set_fill(YELLOW, opacity = 0.2), 
                          square_group2[number_of_cols*(x+1) + (y+1)].animate.set_fill(YELLOW, opacity = 0.5))      
                square_check = VGroup(square_group_check_copy[1], square_group_check_copy[3], square_group_check_copy[4], square_group_check_copy[5], square_group_check_copy[7])
                square_check1 = VGroup(grid1[1], grid1[3], grid1[4], grid1[5], grid1[7])
                square_check2 = VGroup(square_group3[1], square_group3[3], square_group3[4], square_group3[5], square_group3[7])
                a1 = self.check1(grid_text_check, matrix1_check)
                
                if x == 0 and ( y==0 or y==1):   
                    self.play(square_group_check_copy.animate.next_to(grid1, UP*2), run_time = 1)
                    self.wait(0.5)
                    x1 = 0
                    for square1, square2 in zip(square_check, square_check1):
                        self.play(square1[0].animate.set_fill(color = YELLOW, opacity = 0.5),
                                  square2[0].animate.set_fill(color = YELLOW, opacity = 0.5))
                        if text_check1[x1] == 1:
                            self.play(square1[0].animate.set_fill(color = WHITE, opacity = 0.5),
                                      square1[0].animate.set_fill(color = GREEN, opacity = 0.5))
                            self.wait(0.5)
                            self.play(square2[0].animate.set_fill(color = WHITE, opacity = 0.5))
                            x1+=1
                        else:
                            for o in range(3):
                                self.play(square1[0].animate.set_fill(color = WHITE, opacity = 0.5), run_time = 0.5)
                                self.play(square1[0].animate.set_fill(color = RED, opacity = 0.5), run_time = 0.5)
                            self.play(square2[0].animate.set_fill(color = WHITE, opacity = 0.5))
                            break
                else:
                    if a1 == 1:
                        self.play(square_check2.animate.set_fill(color = WHITE, opacity = 0),
                                  square_check2.animate.set_fill(color = GREEN, opacity = 0.5))
                        self.wait(0.5)
                    else:
                        square_check_green = VGroup()
                        square_check_red = VGroup()
                        for x2 in range(5): 
                            if text_check1[x2] == 0:
                                square_check_red.add(square_check2[x2])
                            else:
                                square_check_green.add(square_check2[x2])
                        self.play(square_check2.animate.set_fill(WHITE, opacity = 0),
                                  square_check_red.animate.set_fill(RED, opacity = 0.5),
                                  square_check_green.animate.set_fill(GREEN, opacity = 0.5))
                        self.wait(0.5)       

                s4 = Text(str(a1), color=BLACK, font="SF Pro", font_size=18).move_to(square_group2[number_of_cols*(x+1) + (y+1)].get_center())
                grid2.add(s4)
                self.play(FadeIn(s4))
                self.play(square_group3.animate.set_fill(WHITE, opacity = 0), 
                          square_group2[number_of_cols*(x+1) + (y+1)].animate.set_fill(WHITE, opacity = 0.25),
                          FadeOut(square_group_check_copy))      
        
        self.wait(2)
        self.play(FadeOut(grid1))
        self.play(Group(grid, s1).animate.move_to(LEFT*2.5), Group(grid2, s3).animate.move_to(RIGHT*2.5))
        self.wait(1.5)
        self.play(FadeOut(grid, s1, grid2, s3))
        self.play(FadeIn(img.move_to(ORIGIN))) 
        self.play(FadeIn(eroded_image1.move_to(img.get_center())))
        text1 = Text("Before Erosion", color=BLACK, font="SF Pro", font_size=25).next_to(img, LEFT + UP)
        text2 = Text("After Erosion", color=BLACK, font="SF Pro", font_size=25).next_to(eroded_image1, RIGHT + UP)
        self.play(img.animate.move_to(LEFT*3.5), eroded_image1.animate.move_to(RIGHT*3.5), 
                  Write(text1), Write(text2))    
        self.wait(5)   
    
    def check1(self, matrix3, matrix1):
        if matrix3[0][1] != matrix1[0][1]:
            return 0
        for i in range(3):
            if matrix3[1][i] != matrix1[1][i]:
                return 0
        if matrix3[2][1] != matrix1[2][1]:
            return 0
        return 1