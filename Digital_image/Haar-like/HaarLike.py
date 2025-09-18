from manim import *
import cv2
import numpy
from PIL import Image

class HaarLike(Scene):
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
        txt_header = Text("Haar-like Features", font= "JetBrains Mono", font_size= 38).move_to(ORIGIN).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Succession(Write(txt_header), ApplyWave(txt_header, scale_factor = 1.2), txt_header.animate.to_edge(UP).scale(0.8)))

    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        image = cv2.imread("example.jpg")
        zoomed_image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  
        sharpened_image = cv2.filter2D(zoomed_image, -1, kernel)
        cv2.imwrite("sharpened_image.jpg", sharpened_image)
        
        img = ImageMobject("sharpened_image.jpg")        
        self.play(FadeIn(img.move_to(ORIGIN).shift(UP * 0.5).scale(2)))
        self.wait(0.5)
        self.play(img.animate.move_to(LEFT*1.5))

        red_overlay = Rectangle(width=0.07, height=0.07, color=RED, fill_opacity=0, stroke_width=1)
        overlay_x = 10 * 0.1  
        overlay_y = 16 * 0.1  
        red_overlay.move_to(img.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        matrix = np.array([[1, 2, 2, 4, 1, 5], 
                           [3, 4, 1, 5, 2, 3],
                           [2, 3, 3, 2, 4, 2],
                           [4, 1, 5, 4, 6, 1],
                           [5, 1, 4, 4, 2, 3],
                           [6, 3, 2, 1, 3, 4]])
        grid_original = VGroup()
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid_original.add(VGroup(square, number))
        grid_original.move_to(img.get_corner(UL) + np.array([overlay_x, -overlay_y, 0])).scale(0.01)
        text_original = Text("Input Matrix", color = WHITE, font= "Segoe UI", font_size= 20)
        self.play(FadeIn(grid_original), grid_original.animate.next_to(img, RIGHT*8).scale(100))
        self.play(Write(text_original.next_to(grid_original, UP)))
        self.wait(1)

        self.play(Succession(FadeOut(img, red_overlay),
                             Group(grid_original, text_original).animate.scale(1.4).move_to(LEFT*3)))
        
        #Integral grid
        matrix_integral = [[None for _ in range(number_of_rows)] for _ in range(number_of_cols)]
        grid_integral = VGroup()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                grid_integral.add(square)
        grid_integral.next_to(grid_original, RIGHT*12)
        text_integral = Text("Integral Matrix", color = WHITE, font= "Segoe UI", font_size= 20)
        self.play(Succession(FadeIn(grid_integral.scale(1.4)), Write(text_integral.next_to(grid_integral, UP*1.8).scale(1.4))))

        #Caculate integral grid
        number_integral = VGroup()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                squares_check = VGroup()
                x = self.sum_integral(matrix, i, j)
                matrix_integral[i][j] = x
                number = Text(str(x), color=WHITE, font="SF Pro", font_size=30)
                number_integral.add(number)
                text_sum = Text("SUM = ", font="SF Pro", font_size=30).set_color_by_gradient(PINK, YELLOW, GREEN).next_to(grid_original, DOWN*2).shift(RIGHT*0.4)
                if (i == 0 or i == 1 or i == 1) and (j == 0 or j == 1 or j == 2):
                    for i1 in range(i+1):
                       for j1 in range(j+1):
                           squares_check.add(grid_original[i1*number_of_rows+j1][0])  
                    self.play(squares_check.animate.set_fill(color=WHITE, opacity=0.25),
                              squares_check.animate.set_fill(color=YELLOW, opacity=0.25),
                              grid_integral[number_of_rows*i + j].animate.set_fill(color = WHITE, opacity = 0.35),
                              grid_integral[number_of_rows*i + j].animate.set_fill(color = YELLOW, opacity = 0.35))
                    self.wait(1)
                    texts_group = VGroup()
                    x1 = 0
                    self.play(Write(text_sum))
                    for i1 in range(i+1):
                       for j1 in range(j+1):
                            self.play(grid_original[i1*number_of_rows+j1][0].animate.set_fill(color = BLACK, opacity = 0),
                                      grid_original[i1*number_of_rows+j1][0].animate.set_fill(color = PINK, opacity = 0.5))
                            text_copy = grid_original[i1*number_of_rows+j1][1].copy().set_color_by_gradient(PINK, YELLOW, GREEN).move_to(grid_original[i1*number_of_rows+j1][0].get_center())
                            texts_group.add(text_copy)
                            self.play(text_copy.animate.next_to(text_sum, RIGHT*(x1*2.1 + 1)).scale(1.25), run_time = 0.5)
                            x1+=1
                            if i1 != i or j1 != j:
                                s2 = Text("+", font= "Segoe UI", font_size=30).next_to(text_copy, RIGHT*0.3).set_color_by_gradient(PINK, YELLOW, GREEN)
                                texts_group.add(s2)
                                self.play(Write(s2), run_time = 0.1)

                    s3 = Text("=", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
                    self.play(Write(s3.next_to(text_sum, RIGHT * (2 * x1 + 1))))
                    self.play(Write(number.next_to(s3, RIGHT).set_color_by_gradient(PINK, YELLOW, GREEN)))
                    self.wait(0.5)
                    self.play(number.animate.move_to(grid_integral[number_of_rows*i + j].get_center()).set_color(WHITE).scale(0.9))
                    self.play(squares_check.animate.set_fill(color=BLACK, opacity=0),
                              grid_integral[number_of_rows*i + j].animate.set_fill(color = BLACK, opacity = 0))
                    self.play(FadeOut(texts_group, s3, text_sum))                   
                else:
                    self.play(Write(number.move_to(grid_integral[number_of_rows*i + j].get_center()).scale(0.9), run_time = 0.05)) 
                                   
        self.wait(1)

        #Edge Features
        self.play(FadeOut(grid_original, text_original))
        self.play(Group(grid_integral, text_integral, number_integral).animate.move_to(LEFT*0.2))
        edge_filter = VGroup()
        edge_text = Text("Edge Features", font= "Segoe UI", font_size=24).next_to(text_integral, LEFT*10).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(edge_text))
        white_area = Rectangle(width=square_size * 5.5, height=square_size * 2.8, color=WHITE, fill_opacity=0.8)
        white_area.next_to(edge_text, DOWN)
        edge_filter.add(white_area)
        black_area = Rectangle(width=square_size * 5.5, height=square_size * 2.8, color=GREY, fill_opacity=0.8)
        black_area.next_to(white_area, DOWN, buff=0)
        edge_filter.add(black_area)
        self.play(FadeIn(edge_filter))
        self.play(edge_filter.animate.move_to(grid_integral.get_center()))

        exp_img = ImageMobject("exp.jpg")
        self.play(FadeIn(exp_img.move_to(grid_integral.get_center()).scale(1.55)))
        text_formula = MathTex("S = A + C - B - D", font_size= 30).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(text_formula.next_to(edge_text, DOWN * 2).shift(LEFT*0.2)))
        self.wait(2)
        self.play(FadeOut(exp_img))

        white_group = VGroup()
        text_white = MathTex("S_{white} = ",  font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        self.play(Write(text_white.next_to(text_formula, DOWN * 2).shift(LEFT*1.25)))    
        edge_number = VGroup(number_integral[0].copy(), number_integral[16].copy(), number_integral[4].copy(), number_integral[12].copy())
        white_group.add(text_white, edge_number)
        edge_grid = VGroup(grid_integral[0], grid_integral[16].copy(), grid_integral[4], grid_integral[12])
        for i in range(4):
            if i == 0 or i > 1:
                for j in range(3):
                    self.play(edge_grid[i].animate.set_fill(color = BLACK, opacity=0), run_time = 0.2)
                    self.play(edge_grid[i].animate.set_fill(color = WHITE, opacity=0.5),
                              edge_grid[i].animate.set_fill(color = YELLOW, opacity=0.5),
                              run_time = 0.2)
            else:
                self.play(FadeIn(edge_grid[i].move_to(grid_integral[16].get_center())),
                            edge_grid[i].animate.set_fill( color = YELLOW, opacity = 0.5))
                for j in range(3):
                    self.play(edge_grid[i].animate.set_fill(color = BLACK, opacity=0), run_time = 0.2)
                    self.play(edge_grid[i].animate.set_fill(color = WHITE, opacity=0.5),
                              edge_grid[i].animate.set_fill(color = YELLOW, opacity=0.5),
                              run_time = 0.2)
            self.play(edge_number[i].animate.next_to(text_white, RIGHT * (i*2.9 + 1)).set_color_by_gradient(PINK, YELLOW, GREEN))
            if i == 0 or i >1:
                self.play(edge_grid[i].animate.set_fill(color = WHITE, opacity=0.5),
                        edge_grid[i].animate.set_fill(color = BLACK, opacity=0))
            else:
                self.play(FadeOut(edge_grid[i]))

            if i == 0:
                t_sum = Text("+", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN) 
                white_group.add(t_sum)     
                self.play(Write(t_sum.next_to(edge_number[i], RIGHT*0.9)))
            elif i == 1 or i == 2:
                t_sub = Text("-", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
                white_group.add(t_sub)
                self.play(Write(t_sub.next_to(edge_number[i], RIGHT*0.6)))
        S_edge_number = matrix_integral[0][0] + matrix_integral[0][4] - matrix_integral[2][0] - matrix_integral[2][4]
        s_text = Text(f"=", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        white_group.add(s_text)
        S_edge_text = Text(f"{S_edge_number}", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        self.play(Write(s_text.next_to(text_white, DOWN).shift(RIGHT*0.47), run_time = 0.5))
        self.play(Write(S_edge_text.next_to(s_text, RIGHT)))

        black_group = VGroup()
        text_black = MathTex("S_{black} = ",  font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        self.play(Write(text_black.next_to(text_formula, DOWN * 7).shift(LEFT*1.25)))    
        edge_number1 = VGroup(number_integral[12].copy(), number_integral[28].copy(), number_integral[16].copy(), number_integral[24].copy())
        black_group.add(text_black, edge_number1)
        edge_grid1 = VGroup(grid_integral[12], grid_integral[28].copy(), grid_integral[16].copy(), grid_integral[24])
        for i in range(4):
            if i == 0 or i == 3:
                for j in range(3):
                    self.play(edge_grid1[i].animate.set_fill(color = BLACK, opacity=0), run_time = 0.2)
                    self.play(edge_grid1[i].animate.set_fill(color = WHITE, opacity=0.5),
                              edge_grid1[i].animate.set_fill(color = YELLOW, opacity=0.5),
                              run_time = 0.2)
            elif i == 2:
                self.play(FadeIn(edge_grid1[i].move_to(grid_integral[16].get_center())),
                          edge_grid1[i].animate.set_fill( color = YELLOW, opacity = 0.5))
                for j in range(3):
                    self.play(edge_grid1[i].animate.set_fill(color = BLACK, opacity=0), run_time = 0.2)
                    self.play(edge_grid1[i].animate.set_fill(color = WHITE, opacity=0.5),
                              edge_grid1[i].animate.set_fill(color = YELLOW, opacity=0.5),
                              run_time = 0.2)
            else:
                self.play(FadeIn(edge_grid1[i].move_to(grid_integral[28].get_center())),
                          edge_grid1[i].animate.set_fill( color = YELLOW, opacity = 0.5))
                for j in range(3):
                    self.play(edge_grid1[i].animate.set_fill(color = BLACK, opacity=0), run_time = 0.2)
                    self.play(edge_grid1[i].animate.set_fill(color = WHITE, opacity=0.5),
                              edge_grid1[i].animate.set_fill(color = YELLOW, opacity=0.5),
                              run_time = 0.2)
            self.play(edge_number1[i].animate.next_to(text_black, RIGHT * (i*2.9 + 1)).set_color_by_gradient(PINK, YELLOW, GREEN))
            if i == 0 or i == 3:
                self.play(edge_grid1[i].animate.set_fill(color = WHITE, opacity=0.5),
                        edge_grid1[i].animate.set_fill(color = BLACK, opacity=0))
            else:
                self.play(FadeOut(edge_grid1[i]))

            if i == 0:
                t_sum = Text("+", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN) 
                black_group.add(t_sum)     
                self.play(Write(t_sum.next_to(edge_number1[i], RIGHT*0.9)))
            elif i == 1 or i == 2:
                t_sub = Text("-", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
                black_group.add(t_sub)
                self.play(Write(t_sub.next_to(edge_number1[i], RIGHT*0.6)))
        S_edge_number1 = matrix_integral[2][0] + matrix_integral[4][4] - matrix_integral[2][4] - matrix_integral[4][0]
        s_text1 = Text("=", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        S_edge_text1 = Text(f"{S_edge_number1}", font= "Segoe UI", font_size= 30).set_color_by_gradient(PINK, YELLOW, GREEN)
        black_group.add(s_text1)
        self.play(Write(s_text1.next_to(text_black, DOWN).shift(RIGHT*0.43)))
        self.play(Write(S_edge_text1.next_to(s_text1, RIGHT)))

        text_result = Text("Results", font= "Segoe UI", font_size=24).next_to(text_integral, RIGHT*12).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        text_result1 = MathTex("[ S_{white} ,  S_{black}]", font_size=30).next_to(text_result, DOWN).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Succession(Write(text_result), Write(text_result1)))
        text1 = Text("[       ,      ]", font = "Segoe UI", font_size=24).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(S_edge_text.animate.next_to(text_result1, DOWN * 1.5).shift(LEFT*0.3).scale(0.8),
                  S_edge_text1.animate.next_to(text_result1, DOWN * 1.5).shift(RIGHT*0.4).scale(0.8),
                  FadeIn(text1.next_to(text_result1, DOWN * 1.5)))
        self.wait(1)
        self.play(Succession(FadeOut(white_group, black_group), FadeOut(edge_filter)))

        edge_filter1 = VGroup()
        white_area = Rectangle(width=square_size * 2.8, height=square_size * 5.5, color=WHITE, fill_opacity=0.8)
        white_area.next_to(edge_text, DOWN*5).shift(LEFT*0.8)
        edge_filter1.add(white_area)
        black_area = Rectangle(width=square_size * 2.8, height=square_size * 5.5, color=GREY, fill_opacity=0.8)
        black_area.next_to(white_area, RIGHT, buff=0)
        edge_filter1.add(black_area)
        self.play(FadeIn(edge_filter1))
        self.play(edge_filter1.animate.move_to(grid_integral.get_center()))
        S_edge_number2 = matrix_integral[0][0] + matrix_integral[4][2] - matrix_integral[0][2] - matrix_integral[4][0]
        S_edge_number3 = matrix_integral[0][2] + matrix_integral[4][4] - matrix_integral[0][4] - matrix_integral[4][2]
        text2 = Text(f"[ {S_edge_number2} , {S_edge_number3} ]", font = "Segoe UI", font_size=24).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(text2.next_to(text1, DOWN)))

        self.play(Succession(FadeOut(edge_filter1), FadeOut(edge_text)))

        line_text = Text("Line Features", font= "Segoe UI", font_size=24).next_to(text_integral, LEFT*10).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(line_text))

        line_filter = VGroup()
        white_area = Rectangle(width=square_size * 1.4, height=square_size * 5.5, color=WHITE, fill_opacity=0.8)
        white_area.next_to(line_text, DOWN*5).shift(LEFT)
        line_filter.add(white_area)
        black_area = Rectangle(width=square_size * 2.8, height=square_size * 5.5, color=GREY, fill_opacity=0.8)
        black_area.next_to(white_area, RIGHT, buff=0)
        line_filter.add(black_area)
        white_area1 = white_area.copy()
        white_area1.next_to(black_area, RIGHT, buff=0)
        line_filter.add(white_area1)
        self.play(FadeIn(line_filter))
        self.play(line_filter.animate.move_to(grid_integral.get_center()))
        S_line_number = matrix_integral[0][0] + matrix_integral[4][1] + matrix_integral[0][3] + matrix_integral[4][4] - matrix_integral[0][1] - matrix_integral[4][0] - matrix_integral[0][4] - matrix_integral[4][3]
        S_line_number2 = matrix_integral[0][1] + matrix_integral[4][3] - matrix_integral[0][3] - matrix_integral[4][1]
        text3 = Text(f"[ {S_line_number} , {S_line_number2} ]", font = "Segoe UI", font_size=24).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(text3.next_to(text2, DOWN)))
        self.play(FadeOut(line_filter))

        line_filter1 = VGroup()
        white_area = Rectangle(width=square_size * 5.5, height=square_size * 1.4, color=WHITE, fill_opacity=0.8)
        white_area.next_to(line_text, DOWN*5)
        line_filter1.add(white_area)
        black_area = Rectangle(width=square_size * 5.5, height=square_size * 2.8, color=GREY, fill_opacity=0.8)
        black_area.next_to(white_area, DOWN, buff=0)
        line_filter1.add(black_area)
        white_area1 = white_area.copy()
        white_area1.next_to(black_area, DOWN, buff=0)
        line_filter1.add(white_area1)
        self.play(FadeIn(line_filter1))
        self.play(line_filter1.animate.move_to(grid_integral.get_center()))
        S_line_number = matrix_integral[0][0] + matrix_integral[1][4] + matrix_integral[3][0] + matrix_integral[4][4] - matrix_integral[0][4] - matrix_integral[1][0] - matrix_integral[3][4] - matrix_integral[4][0]
        S_line_number2 = matrix_integral[1][0] + matrix_integral[3][4] - matrix_integral[1][4] - matrix_integral[3][0]
        text4 = Text(f"[ {S_line_number} , {S_line_number2} ]", font = "Segoe UI", font_size=24).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(text4.next_to(text3, DOWN)))
        self.play(Succession(FadeOut(line_filter1), FadeOut(line_text)))

        four_text = Text("Four rectangle Features", font= "Segoe UI", font_size=24).next_to(text_integral, LEFT*7).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(four_text))

        four_filter = VGroup()
        white_area = Rectangle(width=square_size * 2.8, height=square_size * 2.8, color=WHITE, fill_opacity=0.8)
        white_area.next_to(four_text, DOWN*5).shift(RIGHT*0.85)
        four_filter.add(white_area)
        black_area = Rectangle(width=square_size * 2.8, height=square_size * 2.8, color=GREY, fill_opacity=0.8)
        black_area.next_to(white_area, LEFT, buff=0)
        four_filter.add(black_area)
        white_area1 = white_area.copy()
        white_area1.next_to(black_area, DOWN, buff=0)
        four_filter.add(white_area1)
        black_area1 = black_area.copy()
        black_area1.next_to(white_area, DOWN, buff=0)
        four_filter.add(black_area1)
        self.play(FadeIn(four_filter))
        self.play(four_filter.animate.move_to(grid_integral.get_center()))
        S_four_number = matrix_integral[0][2] + matrix_integral[2][4] + matrix_integral[2][0] + matrix_integral[4][2] - matrix_integral[0][4] - matrix_integral[2][2] * 2 - matrix_integral[4][0]
        S_four_number2 = matrix_integral[0][0] + matrix_integral[2][2] * 2 + matrix_integral[4][4] - matrix_integral[0][2] - matrix_integral[2][0] - matrix_integral[2][4] - matrix_integral[4][2]
        text5 = Text(f"[ {S_four_number} , {S_four_number2} ]", font = "Segoe UI", font_size=24).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(text5.next_to(text4, DOWN)))
        self.play(FadeOut(four_filter, four_text))

        self.play(FadeOut(text_formula),
                  Group(grid_integral, text_integral, number_integral).animate.move_to(LEFT*4.5))

        haar_text = Text("Haar Features", font= "Segoe UI", font_size=30).next_to(text_integral, RIGHT*9).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(Write(haar_text))

        self.play(FadeIn(self.create_line().next_to(haar_text, DOWN*1.5)))
        self.play(Succession(Group(text1, S_edge_text, S_edge_text1).animate.next_to(haar_text, DOWN*3),
                             text2.animate.next_to(haar_text, DOWN*5),
                             text3.animate.next_to(haar_text, DOWN*7),
                             text4.animate.next_to(haar_text, DOWN*9),
                             text5.animate.next_to(haar_text, DOWN*11)))
        s4 = VGroup()
        for i in range(3):
            s = Text(".", font= "Segoe UI", font_size=50).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
            s4.add(s)
            self.play(Write(s.next_to(haar_text, DOWN*(13+i)), run_time = 0.5))
        
        self.wait(5)

    def sum_integral(self, matrix, left, right):
        sum = 0
        for i in range(left+1):
            for j in range(right+1):
                sum += matrix[i][j]
        return sum
    
    def create_line(self):
        line1 = Line(start=Dot().move_to(ORIGIN+UP*2+LEFT).get_center(), end=Dot().move_to(ORIGIN+DOWN*1.6+LEFT).get_center(), color=YELLOW)
        line2 = Line(start=Dot().move_to(ORIGIN+UP*2+RIGHT).get_center(), end=Dot().move_to(ORIGIN+DOWN*1.6+RIGHT).get_center(), color=YELLOW)
        line11 = Line(start=Dot().move_to(ORIGIN+UP*2+LEFT*0.5).get_center(), end=Dot().move_to(ORIGIN+UP*2+LEFT).get_center(), color=YELLOW)
        line12 = Line(start=Dot().move_to(ORIGIN+DOWN*1.6+LEFT*0.5).get_center(), end=Dot().move_to(ORIGIN+DOWN*1.6+LEFT).get_center(), color=YELLOW)
        line21 = Line(start=Dot().move_to(ORIGIN+UP*2+RIGHT*0.5).get_center(), end=Dot().move_to(ORIGIN+UP*2+RIGHT).get_center(), color=YELLOW)
        line22 = Line(start=Dot().move_to(ORIGIN+DOWN*1.6+RIGHT*0.5).get_center(), end=Dot().move_to(ORIGIN+DOWN*1.6+RIGHT).get_center(), color=YELLOW)
        line_group = VGroup(line1, line11, line12, line2, line21, line22)
        return line_group