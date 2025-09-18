from manim import *
import cv2
import numpy
from PIL import Image
import operator
import matplotlib.pyplot as plt
from skimage import io

class Erosion(Scene):
    def logo(self):
        image = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg")       
        '# Init logo start at mid of scene'
        image_cp = image.copy().scale(3)  
        image.scale(0.5).to_edge(UP).to_edge(LEFT).shift(LEFT * 0.4, UP * 0.4) 
        self.play(Succession( FadeIn(image_cp), Transform(image_cp, image)))        
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

        image = cv2.imread('example.jpg', 0)  
        kernel = np.ones((5,5), np.uint8)
        eroded_image = cv2.erode(image, kernel, iterations=1)
        cv2.imwrite("eroded_image.jpg", eroded_image)
        eroded_image1 = ImageMobject("eroded_image.jpg").scale(2)

        grid_black = VGroup()
        text_white = VGroup()

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
                if ( matrix[i][j] == 0):
                    grid_black.add(square)
                    text_white.add(number)
                grid.add(VGroup(square, number))
        grid.move_to(ORIGIN).scale(1)
        self.play(FadeIn(grid))
        s1 = Text("Input Matrix", font = "Segoe UI", color = BLACK, font_size= 25).next_to(grid, UP)
        self.play(Write(s1))
        self.play(Circumscribe(s1, color = BLUE, fade_out=True))
        self.wait(1)
        grid_text = Group(grid, s1)
        self.play(grid_text.animate.move_to(LEFT*4))
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
        text_grid2 = VGroup() 
        square_group2 = Group()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                if i == 0 or i == number_of_rows-1 or j == 0 or j == number_of_cols-1:
                    s = Text(str(0), color=BLACK, font="SF Pro", font_size=18).move_to(square.get_center())
                    text_grid2.add(s)
                    grid_black.add(square)
                    text_white.add(s)
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
                text_check1 = [grid_text_check[0][1], grid_text_check[1][0], grid_text_check[1][1], 
                               grid_text_check[1][2], grid_text_check[2][1]]
                for i in range(3):
                    for j in range(3):
                        square_group3.add(grid[(x+i)*number_of_cols + (j+y)][0])
                        square_group_check.add(grid[(x+i)*number_of_cols + (j+y)])
                square_group_check_copy = VGroup(*[obj.copy() for obj in square_group_check])      
                square_check = VGroup(square_group_check_copy[1], square_group_check_copy[3], 
                                      square_group_check_copy[4], square_group_check_copy[5], square_group_check_copy[7])
                square_check1 = VGroup(grid1[1], grid1[3], grid1[4], grid1[5], grid1[7])
                square_check2 = VGroup(square_group_check_copy[1], square_group_check_copy[3], square_group_check_copy[4], 
                                       square_group_check_copy[5], square_group_check_copy[7])
                a1 = self.check1(grid_text_check, matrix1_check)
                s4 = Text(str(a1), color=BLACK, font="SF Pro", font_size=18
                          ).move_to(square_group2[number_of_cols*(x+1) + (y+1)].get_center())
                if a1 == 0:
                    text_white.add(s4)
                    grid_black.add(square_group2[number_of_cols*(x+1) + (y+1)])
                square_check_green = VGroup()
                square_check_red = VGroup()
                if x == 0 and ( y==0 or y==1 or y == 2):  
                    self.play(square_group3.animate.set_fill(YELLOW, opacity = 0.2), 
                          square_group2[number_of_cols*(x+1) + (y+1)].animate.set_fill(YELLOW, opacity = 0.5)) 
                    self.play(square_group_check_copy.animate.next_to(grid1, UP*2), run_time = 1)
                    self.wait(0.5)
                    for x2 in range(5):
                        if text_check1[x2] == 0:
                            square_check_red.add(square_check2[x2])
                        else:
                            square_check_green.add(square_check2[x2])
                    self.play(grid1.animate.move_to(ORIGIN), square_group_check_copy.animate.move_to(ORIGIN))
                    if len(square_check_red) == 0:
                        text_check = Text("Coinciding!", font = "SF Pro", font_size=25
                                          ).next_to(square_group_check_copy, UP).set_color(BLACK)
                        self.play(square.animate.set_fill(color = GREEN, opacity=0.5) for square in square_check_green)
                        self.play(Succession(Write(text_check), Indicate(text_check, color=GREEN_D), FadeOut(text_check)))
                    else:
                        text_check = Text("Not Coinciding!", font = "SF Pro", font_size=25
                                          ).next_to(square_group_check_copy, UP).set_color(BLACK)
                        self.play(square_check_red.animate.set_fill(color = RED, opacity=0.5),
                                  square_check_green.animate.set_fill(color = GREEN, opacity=0.5))
                        for i in range(3):
                            self.play(square_check_red.animate.set_fill(color = WHITE, opacity=0.5), run_time = 0.5)
                            self.play(square_check_red.animate.set_fill(color = RED_D, opacity=0.5), run_time = 0.5)
                        self.play(Succession(Write(text_check), Indicate(text_check, color=RED_D), FadeOut(text_check)))     
                grid2.add(s4)
                
                if x == 0 and ( y == 0 or y == 1 or y == 2):
                    self.play(FadeIn(s4))
                    self.play(square_group3.animate.set_fill(WHITE, opacity = 0), 
                            square_group2[number_of_cols*(x+1) + (y+1)].animate.set_fill(WHITE, opacity = 0.25),
                            FadeOut(square_group_check_copy),
                            grid1.animate.move_to(ORIGIN + DOWN*1.5))      
                    self.wait(1)
                else:
                    self.play(FadeIn(s4, run_time=0.1))
        
        self.wait(0.5)
        self.play(FadeOut(grid1))
        self.play(FadeIn(text_grid2.move_to(grid2.get_center())))
        self.play(Group(grid, s1).animate.move_to(LEFT*2.5), 
                  Group(grid2, s3, text_grid2).animate.move_to(RIGHT*2.5))
        self.play(grid_black.animate.set_fill(color = BLACK, opacity = 1), 
                  text_white.animate.set_color(WHITE), run_time = 2)
        self.wait(2)
        self.play(FadeOut(grid, s1, grid2, s3, text_grid2))
        s5 = Text("Original Image", color=BLACK, font="SF Pro", font_size=25)
        self.play(Succession(FadeIn(img.move_to(ORIGIN+DOWN*0.01).scale(1.1), run_time=2), 
                             Write(s5.next_to(img, UP))))
        self.play(Wiggle(s5, scale_value=1.2, rotation_angle=0.05))
        self.play(FadeOut(s5))
        self.play(FadeIn(eroded_image1.move_to(img.get_center()).scale(1.1)),  
                  lag_ratio=0.1, run_time = 1)        
        text1 = Text("Before Erosion", color=BLACK, font="SF Pro", font_size=25
                     ).next_to(img, LEFT*0.5 + UP)
        text2 = Text("After Erosion", color=BLACK, font="SF Pro", font_size=25
                     ).next_to(eroded_image1, RIGHT*0.5 + UP)
        self.play(img.animate.move_to(LEFT*3.5), 
                  eroded_image1.animate.move_to(RIGHT*3.5), 
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