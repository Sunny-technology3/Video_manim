from manim import *
import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt

class LBPH(Scene):
    def logo(self):
        image = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg")       
        '# Init logo start at mid of scene'
        image_cp = image.copy().scale(3)  
        image.scale(0.5).to_edge(UP).to_edge(LEFT).shift(LEFT * 0.4, UP * 0.4) 
        self.play(Succession( FadeIn(image_cp), Transform(image_cp, image)))        
        txt_intro = Text('''STDR2024 @EIC&DSP LAB\nDesigned by Le Minh Nam''',
                        font= "Segoe UI", font_size= 20
                        ).scale(2).move_to(ORIGIN)
        txt_intro.set_color(WHITE)
        self.play(Write(txt_intro), run_time = 1.5)
        self.play(txt_intro.animate.scale(0.3).to_edge(DR).shift(DOWN * 0.35, RIGHT * 0.35))
        txt_header = Text("Local Binary Pattern Histogram", font= "JetBrains Mono", font_size= 38).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).move_to(ORIGIN)
        self.play(Succession(Write(txt_header), ApplyWave(txt_header, scale_factor = 1.2), txt_header.animate.to_edge(UP).scale(0.8)))
    
    def compute_lbp(self, image):
        rows, cols = image.shape
        lbp_image = np.zeros_like(image, dtype=np.uint8)

        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                center = image[r, c]
                binary_string = ''

                binary_string += '1' if image[r - 1, c - 1] > center else '0'  
                binary_string += '1' if image[r - 1, c] > center else '0'      
                binary_string += '1' if image[r - 1, c + 1] > center else '0' 
                binary_string += '1' if image[r, c + 1] > center else '0'      
                binary_string += '1' if image[r + 1, c + 1] > center else '0' 
                binary_string += '1' if image[r + 1, c] > center else '0'      
                binary_string += '1' if image[r + 1, c - 1] > center else '0'  
                binary_string += '1' if image[r, c - 1] > center else '0'     

                lbp_value = int(binary_string, 2)
                lbp_image[r, c] = lbp_value

        return lbp_image

    def calculate_histogram(self, lbp_image):
        hist, _ = np.histogram(lbp_image, bins=256, range=(0, 256))
        return hist

    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        img = cv2.imread("example.jpg")
        original_image = ImageMobject("example.jpg").scale(2)
        original_text_img = Text("Original Image", font= "Segoe UI", font_size= 22).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Succession(FadeIn(original_image), original_image.animate.shift(LEFT * 3)))
        self.wait(1)

        gray_image = cv2.imread("example.jpg", cv2.IMREAD_GRAYSCALE)
        lbp_image = self.compute_lbp(gray_image)
        lbp_histogram = self.calculate_histogram(lbp_image)
        Image.fromarray(lbp_image).save("lbp_image.jpg")
        plt.figure(figsize=(5, 3), facecolor='black')
        plt.bar(range(256), lbp_histogram, color='white')
        plt.gca().set_facecolor('black')
        plt.tick_params(colors='white') 
        plt.savefig("lbp_histogram.jpg", bbox_inches='tight')
        plt.close()
        lbp_image_mobject = ImageMobject("lbp_image.jpg").scale(2)
        lbp_text_img = Text("LBP Image", font= "Segoe UI", font_size= 22).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        hist_image_mobject = ImageMobject("lbp_histogram.jpg").scale(2)
        lbph_text_img = Text("LBP Histogram", font= "Segoe UI", font_size= 20).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)

        red_overlay = Rectangle(width=1.2 * 0.1, height=1.2 * 0.1, color=RED, fill_opacity=0)
        overlay_x = 16 * 0.1  
        overlay_y = 12.5 * 0.1  
        red_overlay.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        #original grid
        cropped_img = img[250:257, 250:257]
        gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        matrix = np.array(gray_img)
        original_grid = VGroup()
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                original_grid.add(VGroup(square, number))
        original_grid.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0])).scale(0.01)
        self.play(FadeIn(original_grid), original_grid.animate.next_to(original_image, RIGHT*10).scale(110))
        original_text = Text("Original Grid", font= "Segoe UI", font_size= 22).next_to(original_grid, UP).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Write(original_text))
        self.play(Succession(FadeOut(original_image, red_overlay), Group(original_text, original_grid).animate.move_to(LEFT * 4).scale(0.95)))

        #LBP grid
        lbp_grid = VGroup()
        empty_square = VGroup()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                if i == 0 or j == 0 or i == number_of_rows-1 or j == number_of_cols-1:
                    empty_square.add(square)
                else:
                    lbp_grid.add(square)
        lbp_grid.next_to(original_grid, RIGHT * 17.5)
        empty_square.move_to(lbp_grid.get_center())
        
        lbp_text = Text("LBP Grid", font= "Segoe UI", font_size= 22).next_to(lbp_grid, UP*3.5).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Succession(FadeIn(lbp_grid, empty_square), Write(lbp_text)))

        lbp_grid_result = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                lbp_grid_result.add(square)
        lbp_group_check = VGroup()
        for i in range(3):
            lbp_group_check.add(lbp_grid_result[i])
        for i in range(2):
            lbp_group_check.add(lbp_grid_result[2+3*(i+1)])
        for i in range(2):
            lbp_group_check.add(lbp_grid_result[7-i])
        lbp_group_check.add(lbp_grid_result[3])
        
        number_result_group = VGroup()
        number_result_matrix = [0 for _ in range((number_of_rows-2)*(number_of_cols-2))]
        cnt = 0
        for x in range(number_of_rows-2):
            for y in range(number_of_cols-2):               
                matrix_check = self.matrix_check_number(matrix, x, y)
                number_result1 = self.binary(matrix_check)
                number_result_matrix[cnt] = number_result1
                cnt+=1
                text_number_result = Text(f"{number_result1}", color=WHITE, font= "Segoe UI", font_size= 20)
                number_result_group.add(text_number_result)
                if x == 0 and y == 0:
                    square_group_check = VGroup()
                    for i in range(3):
                        square_group_check.add(original_grid[x*number_of_cols + (i+y)])
                    for i in range(2):
                        square_group_check.add(original_grid[(x+i+1)*number_of_cols + (2+y)])
                    for i in range(2):
                        square_group_check.add(original_grid[(x+2)*number_of_cols + (y-i+1)])
                    square_group_check.add(original_grid[(x+1)*number_of_cols + y])
                    square_group_check.add(original_grid[(x+1)*number_of_cols + y+1])
                    square_group_check1 = VGroup()
                    for square in square_group_check:
                        square_group_check1.add(square[0])
                    square_group_check_copy = VGroup(*[obj.copy() for obj in square_group_check])
                    self.play(square_group_check1.animate.set_fill(color = YELLOW, opacity=0.5),
                              lbp_grid[(number_of_cols - 2)*x + y].animate.set_fill(YELLOW, opacity = 0.5))
                    self.play(square_group_check_copy.animate.move_to(ORIGIN).shift(UP))
                    text_group_check = VGroup()
                    for square in square_group_check_copy:
                        text_group_check.add(square[1])
                    text_group_check_copy = VGroup(*[obj.copy() for obj in text_group_check])
                    self.play(FadeIn(lbp_grid_result.next_to(square_group_check_copy, DOWN*5)))
                    self.play(square_group_check_copy[len(square_group_check_copy)-1].animate.set_fill(color = PINK, opacity = 0.6))
                    number_result = VGroup()
                    for i in range(len(square_group_check_copy) - 1):
                        x1 = self.check(matrix_check[i], matrix_check[8])
                        s_x = Text(f"{x1}", color=WHITE, font= "Segoe UI", font_size= 20)
                        if i<4:
                            self.play(square_group_check_copy[i].animate.set_fill(color=YELLOW, opacity = 0.5))
                            self.play(text_group_check_copy[i].animate.move_to(ORIGIN).shift(LEFT*0.5 + DOWN*0.5),
                                    text_group_check_copy[8].animate.move_to(ORIGIN).shift(RIGHT*0.5 + DOWN*0.5))
                            self.wait(1)                     
                            if matrix_check[i] > matrix_check[8]:
                                text_ss = Text(">", color=WHITE, font= "Segoe UI", font_size= 23)
                                self.play(Succession(Write(text_ss.move_to(ORIGIN).shift(DOWN*0.5)),
                                            Indicate(text_ss, color=GREEN)))
                            elif matrix_check[i] == matrix_check[8]:
                                text_ss = Text("=", color=WHITE, font= "Segoe UI", font_size= 23)
                                self.play(Succession(Write(text_ss.move_to(ORIGIN).shift(DOWN*0.5)),
                                            Indicate(text_ss, color=GREEN)))
                            else:
                                text_ss = Text("<", color=WHITE, font= "Segoe UI", font_size= 23)
                                self.play(Succession(Write(text_ss.move_to(ORIGIN).shift(DOWN*0.5)),
                                            Indicate(text_ss, color=RED)))
                            if x1 == 1:
                                self.play(lbp_group_check[i].animate.set_fill(color=GREEN, opacity=0.5))
                            else:
                                self.play(lbp_group_check[i].animate.set_fill(color=RED, opacity=0.5))
                            self.play(Write(s_x.move_to(lbp_group_check[i].get_center())))
                            number_result.add(s_x)                
                            self.play(lbp_group_check[i].animate.set_fill(color=BLACK, opacity=0))
                            self.play(FadeOut(text_ss),
                                    text_group_check_copy[i].animate.move_to(square_group_check_copy[i][0].get_center()), 
                                    text_group_check_copy[8].animate.move_to(square_group_check_copy[8][0].get_center()),
                                    square_group_check_copy[i].animate.set_fill(color=BLACK, opacity = 0))
                        else:
                            self.play(Write(s_x.move_to(lbp_group_check[i].get_center()), run_time = 0.1))
                            number_result.add(s_x)
                    number_result_copy = VGroup(*[obj.copy() for obj in number_result])    
                    self.wait(1)
                    text_binary = Text("Binary Number :", font= "Segoe UI", font_size= 26).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
                    self.play(Write(text_binary.move_to(ORIGIN).shift(DOWN*3 + LEFT*4)))
                    for i in range(len(number_result_copy)):
                        self.play(lbp_group_check[i].animate.set_fill(color=BLUE, opacity = 0.5), run_time = 0.4)
                        self.play(number_result_copy[i].animate.next_to(text_binary, RIGHT * (i+0.5)).scale(1.1).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN),
                                  run_time = 0.6)
                    decimal_text = Text("Decimal Number :", font= "Segoe UI", font_size= 26).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
                    self.play(Write(decimal_text.move_to(ORIGIN).shift(DOWN*3 + RIGHT*2)))
                    self.play(Write(text_number_result.next_to(decimal_text, RIGHT).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).scale(1.1)))
                    self.play(text_number_result.animate.move_to(lbp_grid[(number_of_cols - 2)*x + y].get_center()).set_color(WHITE).scale(0.9))
                    self.wait(1)
                    self.play(square_group_check1.animate.set_fill(color = BLACK, opacity=0),
                              lbp_grid[(number_of_cols - 2)*x + y].animate.set_fill(BLACK, opacity = 0),
                              FadeOut(lbp_grid_result, text_group_check_copy, text_binary,
                                      decimal_text, number_result_copy, number_result, square_group_check_copy))
                    self.play(Group(original_grid, original_text).animate.shift(RIGHT),
                              Group(lbp_grid, lbp_text, text_number_result, empty_square).animate.shift(LEFT))
                else:
                    self.play(Write(text_number_result.move_to(lbp_grid[(number_of_cols - 2)*x + y].get_center()), run_time = 0.1))

        self.wait(1)
        self.play(FadeOut(original_grid, original_text))
        
        self.play(Group(lbp_grid, text_number_result, number_result_group).animate.move_to(ORIGIN+LEFT*4.5),
                  lbp_text.animate.move_to(ORIGIN+LEFT*4.5 + UP*1.5), 
                  FadeOut(empty_square, run_time = 0.1))
        
        histogram_dict = self.count_frequencies(number_result_matrix)
        #LBPH grid
        lbph_grid = VGroup()
        for i in range(2):
            for j in range(len(histogram_dict)):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                lbph_grid.add(square)
        lbph_grid.move_to(ORIGIN).shift(RIGHT*2+UP*1.2)
        lbph_text = Text("Frequency Table", font= "Segoe UI", font_size= 22).next_to(lbph_grid, UP*1.5).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(FadeIn(lbph_grid),
                  Write(lbph_text))
        
        number_group = VGroup()
        for number, i in zip(histogram_dict, range(len(histogram_dict))):
            s1 = Text(f"{number}", color=WHITE, font= "Segoe UI", font_size= 20).move_to(lbph_grid[i].get_center())
            number_group.add(s1)
            self.play(Write(s1), run_time = 0.1)

        axes = Axes(
            x_range=[0, 70, 1],
            y_range=[0, 6, 1],
            axis_config={"color": BLUE},
            y_length=10,
            x_length=9,
            x_axis_config={
                "tick_size": 0.05,  
            },
            y_axis_config={
                "tick_size": 0.05,
            }
        ).scale(0.4)
        axes.next_to(lbph_grid, DOWN*0.75)
        self.play(FadeIn(axes))

        stems = VGroup()
        lbph_number = VGroup()
        for number, i in zip(histogram_dict, range(len(histogram_dict))):
            frequencies_number = histogram_dict.get(number)           
            s1 = Text(f"{frequencies_number}", color=WHITE, font= "Segoe UI", font_size= 20).move_to(lbph_grid[len(histogram_dict) + i].get_center())
            lbph_number.add(s1)
            line = Line(axes.c2p(float(number/5), 0), axes.c2p(float(number/5), frequencies_number), color=GREEN)         
            stems.add(line)
            if i<4:
                square_check = self.square_number(number, number_result_matrix, lbp_grid)
                self.play(lbph_grid[i].animate.set_fill(color=RED, opacity=0.5))
                self.play(square_check.animate.set_fill(color=YELLOW, opacity=0.5))
                self.play(Write(s1), run_time = 0.5)
                self.play(lbph_grid[i].animate.set_fill(color=BLACK, opacity=0),
                          square_check.animate.set_fill(color=BLACK, opacity=0))
                self.play(Create(line))
            else:
                self.play(Write(s1), run_time = 0.3)
                self.play(Create(line, run_time = 0.3))
        self.wait(1.5)

        self.play(FadeOut(lbp_grid, text_number_result, number_result_group, lbp_text,lbph_grid, number_group, 
                          lbph_number, lbph_text, axes, stems))
        original_image.move_to(ORIGIN)
        self.play(FadeIn(original_image),
                  Write(original_text_img.next_to(original_image, UP).scale(1.1)))
        self.wait(1)
        self.play(FadeIn(lbp_image_mobject.move_to(original_image.get_center()), run_time = 0.2))
        self.play(FadeOut(original_text_img, original_image), run_time = 0.05)
        self.wait(0.5)
        self.play(Write(lbp_text_img.next_to(lbp_image_mobject, UP).scale(1.1)))
        self.play(Group(lbp_image_mobject, lbp_text_img).animate.move_to(LEFT*4))
        self.play(FadeIn(hist_image_mobject.next_to(lbp_image_mobject, RIGHT*3)))
        self.play(Write(lbph_text_img.next_to(hist_image_mobject, UP*0.6)))
        self.wait(5)
    
    def square_number(self, number, matrix, square_group):
        square_check = VGroup()
        for i in range(len(matrix)):
            if number == matrix[i]:
                square_check.add(square_group[i])
        return square_check

    def count_frequencies(self, matrix):
        frequency_dict = {}
        for number in matrix:
            if number in frequency_dict:
                frequency_dict[number] += 1
            else:
                frequency_dict[number] = 1
        return frequency_dict
    
    def check(self, a, b):
        if a>=b:
            return 1
        return 0
        
    def binary(self, matrix):
        number = 0
        x = len(matrix)
        last_element = matrix[x - 1]
        for i in range(x - 1):
            if matrix[i] >= last_element:
                number += pow(2, x - 2 - i)
        return number
        
    def matrix_check_number(self, matrix, x, y):
        x1 = 0
        matrix_check = [0 for _ in range(9)] 
        for i in range(3):
            matrix_check[x1] = matrix[x][y+i]
            x1+=1
        for i in range(2):
            matrix_check[x1] = matrix[x+i+1][y+2] 
            x1+=1
        for i in range(2):
            matrix_check[x1] = matrix[x+2][y+1-i]
            x1+=1
        matrix_check[x1] = matrix[x+1][y]
        matrix_check[x1+1] = matrix[x+1][y+1]
        return matrix_check