from manim import *
import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import exposure, io
import math

class HOG(Scene):
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
        txt_header = Text("Histogram of oriented gradients",font= "JetBrains Mono", font_size= 38).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN).move_to(ORIGIN)
        self.play(Succession(Write(txt_header), ApplyWave(txt_header, scale_factor = 1.2), txt_header.animate.to_edge(UP).scale(0.8)))

    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        img = cv2.imread("example.jpg")
        original_image = ImageMobject("example.jpg").scale(1.2)
        self.play(Succession(FadeIn(original_image), original_image.animate.shift(LEFT * 3)))
        self.wait(1)

        red_overlay = Rectangle(width=4.5 * 0.1, height=9 * 0.1, color=RED, fill_opacity=0)
        overlay_x = 30 * 0.1  
        overlay_y = 19 * 0.1  
        red_overlay.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        cropped_img = img[165:260, 315:362]
        cv2.imwrite("cropped_example.jpg", cropped_img)

        cropped_image_mobject = ImageMobject("cropped_example.jpg")
        cropped_image_mobject.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Succession(FadeIn(cropped_image_mobject, run_time = 0.1),
                             cropped_image_mobject.animate.next_to(original_image, RIGHT*6).scale(6.5)))
     
        arrow_up1 = self.create_arrow_up(cropped_image_mobject)
        arrow_text1 = Text("64", font = "Segoe UI", font_size=20, color=YELLOW)
        arrow_text1.next_to(arrow_up1, UP*0.3)
        self.play(Succession(Create(arrow_up1), Write(arrow_text1)))

        arrow_right1 = self.create_arrow_right(cropped_image_mobject)
        arrow_text2 = Text("128", font = "Segoe UI", font_size=20, color=YELLOW)
        arrow_text2.next_to(arrow_right1, RIGHT*0.3)
        self.play(Succession(Create(arrow_right1), Write(arrow_text2)))

        arrow_group = VGroup(arrow_right1, arrow_text1, arrow_text2, arrow_up1)
        self.wait(1)

        vertical_spacing = cropped_image_mobject.width / 8
        horizontal_spacing = cropped_image_mobject.height / 16
        grid_lines = VGroup()
        for i in range(1, 8):
            line = Line(
                start=cropped_image_mobject.get_top() + LEFT * (cropped_image_mobject.width / 2) + RIGHT * i * vertical_spacing,
                end=cropped_image_mobject.get_bottom() + LEFT * (cropped_image_mobject.width / 2) + RIGHT * i * vertical_spacing,
                stroke_width=1,
                color=PURPLE_E
            )
            grid_lines.add(line)
        for i in range(1, 16):
            line = Line(
                start=cropped_image_mobject.get_left() + DOWN * (cropped_image_mobject.height / 2) + UP * i * horizontal_spacing,
                end=cropped_image_mobject.get_right() + DOWN * (cropped_image_mobject.height / 2) + UP * i * horizontal_spacing,
                stroke_width=1,
                color=PURPLE_E
            )
            grid_lines.add(line)
        grid_lines.move_to(cropped_image_mobject)
        self.play(Create(grid_lines))
        self.wait(1)

        target_cell = cropped_img[35:43,:8]        
        cv2.imwrite("target_cell.jpg", target_cell)
        target_cell_image = ImageMobject("target_cell.jpg").scale(5.5)
        self.play(Succession(FadeIn(target_cell_image.move_to(cropped_image_mobject.get_left()).shift(UP*0.35 + RIGHT*0.15), run_time = 0.1),
                             target_cell_image.animate.next_to(cropped_image_mobject, RIGHT*7.5).scale(5)))
        
        arrow_up2 = self.create_arrow_up(target_cell_image)
        arrow_text12 = Text("8", font = "Segoe UI", font_size=20, color=YELLOW)
        arrow_text12.next_to(arrow_up2, UP*0.3)
        self.play(Succession(Create(arrow_up2), Write(arrow_text12)))

        arrow_right2 = self.create_arrow_right(target_cell_image)
        arrow_text22 = Text("8", font = "Segoe UI", font_size=20, color=YELLOW)
        arrow_text22.next_to(arrow_right2, RIGHT*0.3)
        self.play(Succession(Create(arrow_right2), Write(arrow_text22)))

        arrow_group.add(arrow_right2, arrow_text12, arrow_text22, arrow_up2)
        self.wait(1)
        self.play(FadeOut(original_image, grid_lines, red_overlay, cropped_image_mobject, arrow_group),
                  target_cell_image.animate.move_to(LEFT * 4).scale(2.5))
           
        image = cv2.imread("target_cell.jpg", cv2.IMREAD_GRAYSCALE)
        gradient_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  
        gradient_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)  
        magnitude = cv2.magnitude(gradient_x, gradient_y)
        direction = cv2.phase(gradient_x, gradient_y, angleInDegrees=True)

        gray_img = cv2.cvtColor(target_cell, cv2.COLOR_BGR2GRAY)
        matrix = np.array(gray_img)
        grid = VGroup()
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid.add(VGroup(square, number))
        grid.move_to(target_cell_image.get_center())
        original_text_grid = Text("Original Matrix", font = "Segoe UI", font_size= 25).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(FadeIn(grid), grid.animate.move_to(RIGHT*2.5))
        self.play(Write(original_text_grid.next_to(grid, UP)))
        self.play(FadeOut(target_cell_image),
                  Group(grid, original_text_grid).animate.move_to(LEFT*4.5))

        matrix1_check = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        matrix1 = np.array([[-1, 0, 1], 
                            [-2, 0, 2], 
                            [-1, 0, 1]])
        grid1 = VGroup()
        number_of_cols1 = len(matrix1[0])
        number_of_rows1 = len(matrix1)
        for i in range(number_of_rows1):
            for j in range(number_of_cols1):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix1[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid1.add(VGroup(square, number))

        matrix2_check = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        matrix2 = np.array([[-1, -2, -1], 
                            [0, 0, 0], 
                            [1, 2, 1]])
        grid2 = VGroup()
        for i in range(number_of_rows1):
            for j in range(number_of_cols1):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix2[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid2.add(VGroup(square, number))
        
        gradient_magnitude = VGroup()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                gradient_magnitude.add(square)
        gradient_magnitude.next_to(grid, RIGHT * 2)
        gradient_magnitude_text = Text("Gradient Magnitude", font = "Segoe UI", font_size= 23).next_to(gradient_magnitude, UP).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)

        gradient_direction = VGroup()
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                gradient_direction.add(square)
        gradient_direction.next_to(gradient_magnitude, RIGHT*2)
        gradient_direction_text = Text("Gradient Direction", font = "Segoe UI", font_size= 23).next_to(gradient_direction, UP).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)

        square_group_check = VGroup()
        square_group_check1 = VGroup()
        grid_text_check = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                grid_text_check[i][j] = matrix[i][j]
        for i in range(3):
            for j in range(3):
                square_group_check.add(grid[i*number_of_cols + j])
                square_group_check1.add(grid[i*number_of_cols + j][0])
        square_group_check_copy = VGroup(*[obj.copy() for obj in square_group_check])      
        Ix = self.sobel(matrix1_check, grid_text_check)
        Iy = self.sobel(matrix2_check, grid_text_check)
        M = round(math.sqrt(pow(Ix, 2) + (pow(Iy, 2))))
        alpha = self.direction(Iy, Ix)
        M_text_group = VGroup()
        M_text = Text(f"{M}", font = "Segoe UI", color=WHITE, font_size = 23)
        M_text_group.add(M_text)
        alpha_text_group = VGroup()
        alpha_text = Text(f"{alpha}", font = "Segoe UI", color=WHITE, font_size = 23)
        alpha_text_group.add(alpha_text)

        self.play(square_group_check1.animate.set_fill(color=YELLOW, opacity=0.5))
        self.play(square_group_check_copy.animate.next_to(grid, RIGHT*2))
        square_group_check_copy1 = VGroup(*[obj.copy() for obj in square_group_check_copy])
        self.play(FadeIn(grid1.move_to(ORIGIN + UP + RIGHT * 4)))
        self.play(square_group_check_copy1.animate.next_to(grid1, LEFT))
        s1 = Text("*", color=WHITE, font="SF Pro", font_size=18).next_to(square_group_check_copy1, RIGHT*0.25)
        self.play(Write(s1))
        self.wait(0.5)
        self.play(FadeOut(s1),
                    square_group_check_copy1.animate.move_to(s1.get_center()),
                    grid1.animate.move_to(s1.get_center()))
        grid1_result = VGroup()
        for i in range(number_of_rows1):
            for j in range(number_of_cols1):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix1[i][j]*grid_text_check[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid1_result.add((VGroup(number, square)))
        self.play((FadeOut(square_group_check_copy1, grid1),
                    FadeIn(grid1_result.move_to(grid1.get_center()))))
        Ix_text = MathTex(f"I_x = {Ix}", color=WHITE, font_size = 25)
        self.play(Write(Ix_text.next_to(grid1_result, DOWN)))

        square_group_check_copy2 = VGroup(*[obj.copy() for obj in square_group_check_copy])
        self.play(FadeIn(grid2.move_to(ORIGIN + DOWN * 1.5 + RIGHT * 4)))
        self.play(square_group_check_copy2.animate.next_to(grid2, LEFT))
        s2 = Text("*", color=WHITE, font="SF Pro", font_size=18).next_to(square_group_check_copy2, RIGHT*0.25)
        self.play(Write(s2))
        self.wait(0.5)
        self.play(FadeOut(s2),
                    square_group_check_copy2.animate.move_to(s2.get_center()),
                    grid2.animate.move_to(s2.get_center()))
        grid2_result = VGroup()
        for i in range(number_of_rows1):
            for j in range(number_of_cols1):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix1[i][j]*grid_text_check[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid2_result.add((VGroup(number, square)))
        self.play((FadeOut(square_group_check_copy2, grid2),
                    FadeIn(grid2_result.move_to(grid2.get_center()))))
        Iy_text = MathTex(f"I_y = {Iy}", color=WHITE, font_size = 25)
        self.play(Write(Iy_text.next_to(grid2_result, DOWN)))
        self.play(FadeOut(grid1_result, grid2_result, square_group_check_copy),
                    Ix_text.animate.move_to(ORIGIN + UP*2),
                    Iy_text.animate.move_to(ORIGIN + UP*1.5))
        M_result = MathTex(r"M = \sqrt{I_x^2 + I_y^2} = ", color=WHITE, font_size = 25).next_to(Iy_text, DOWN)
        self.play(Succession(Write(M_result),
                             Write(M_text.next_to(M_result, RIGHT))))
        alpha_result = MathTex(r"\alpha = arctan(\frac{I_y}{I_x}) = ", color=WHITE, font_size = 25).next_to(Iy_text, DOWN*3)
        self.play(Succession(Write(alpha_result),
                             Write(alpha_text.next_to(alpha_result, RIGHT))))
        
        self.play(FadeOut(Ix_text, Iy_text),
                    Group(M_text, M_result).animate.next_to(gradient_magnitude_text, UP*0.9),
                    Group(alpha_text, alpha_result).animate.next_to(gradient_direction_text, UP*0.9))
        self.play(Succession(FadeIn(gradient_magnitude), Write(gradient_magnitude_text)))
        self.play(M_text.animate.move_to(gradient_magnitude[number_of_cols + 1].get_center()).scale(0.8),
                  FadeOut(M_result))
        self.play(Succession(FadeIn(gradient_direction), Write(gradient_direction_text)))
        self.play(alpha_text.animate.move_to(gradient_direction[number_of_cols + 1].get_center()).scale(0.8),
                  FadeOut(alpha_result))
        self.play(square_group_check1.animate.set_fill(color=BLACK, opacity=0))

        for x in range(number_of_cols):
            for y in range(number_of_rows):
                if x != 1 or y != 1:
                    M_text = Text(f"{round(magnitude[x][y])}", font = "Segoe UI", color=WHITE, font_size = 23)
                    M_text_group.add(M_text)
                    alpha_text = Text(f"{round(direction[x][y])}", font = "Segoe UI", color=WHITE, font_size = 23)
                    alpha_text_group.add(alpha_text)
                    self.play(Write(M_text.move_to(gradient_magnitude[x*number_of_cols + y].get_center()).scale(0.8), run_time = 0.1),
                              Write(alpha_text.move_to(gradient_direction[x*number_of_cols + y].get_center()).scale(0.8), run_time = 0.1))

        self.play(FadeOut(grid, original_text_grid),
                  Group(gradient_magnitude, gradient_magnitude_text, M_text_group).animate.move_to(LEFT*4.7).scale(0.95),
                  Group(gradient_direction, gradient_direction_text, alpha_text_group).animate.move_to(RIGHT*4.7).scale(0.95))
        
        grid_hog = VGroup()
        alpha_group = VGroup()
        M_group = VGroup()
        alpha = 0
        for i in range(2):
            for j in range(10):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                if i == 0 and j == 0:
                    number =  MathTex(r"\alpha", color=WHITE, font_size = 18).move_to(square.get_center())
                    grid_hog.add(VGroup(square, number))
                elif i == 1 and j == 0:
                    number = Text("M", color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                    grid_hog.add(VGroup(square, number))
                else:
                    if i == 0:
                        number = Text(f"{alpha}", color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                        alpha_group.add(number)
                        alpha+=20
                    else:
                        number = Text("0", color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                        M_group.add(number)
                    grid_hog.add(square)
        hog_text = Text("Histogram of Gradients", font = "Segoe UI", font_size = 23).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(FadeIn(Group(grid_hog, alpha_group, M_group).move_to(ORIGIN+DOWN*2)))
        self.play(Write(hog_text.next_to(grid_hog, DOWN)))
        self.wait(1)

        m_text = Text("M:", color = WHITE, font = "Segoe UI", font_size = 25)
        alp_text = MathTex(r"\alpha:", color=WHITE, font_size = 45)
        x1 = 0
        for i in range(3):
            x1 += magnitude[0][i]
            histogram_text = Text(f"{round(x1)}", color=WHITE, font="SF Pro", font_size=18)
            square_magnitude = gradient_magnitude[i].copy()
            number_magnitude = M_text_group[i+1].copy()
            square_direction = gradient_direction[i].copy()
            number_direction = alpha_text_group[i+1].copy()
            check_group = VGroup(square_direction, square_magnitude, number_direction)
            self.play(gradient_magnitude[i].animate.set_fill(color = YELLOW, opacity = 0.5),
                      gradient_direction[i].animate.set_fill(color = YELLOW, opacity = 0.5))
            if i == 0:    
                self.play(Write(alp_text.move_to(ORIGIN + UP*1.5 + LEFT*1.5)))
            self.play(Group(square_direction, number_direction).animate.next_to(alp_text, RIGHT).scale(1.2))
            for j in range(3):
                self.play(grid_hog[1].animate.set_fill(color=BLACK, opacity = 0), run_time = 0.1)
                self.play(grid_hog[1].animate.set_fill(color=YELLOW, opacity = 0.5), run_time = 0.1)
            if i == 0:
                self.play(Write(m_text.move_to(ORIGIN + UP*1.5 + RIGHT*0.5)))
            self.play(Group(square_magnitude, number_magnitude).animate.next_to(m_text, RIGHT).scale(1.2))
            self.play(number_magnitude.animate.move_to(grid_hog[11].get_center()))
            self.play(FadeOut(Group(M_group[0], number_magnitude)),
                      FadeIn(histogram_text.move_to(grid_hog[11].get_center())))
            M_group.submobjects.pop(0)
            M_group.add_to_back(histogram_text)
            self.play(gradient_magnitude[i].animate.set_fill(color = BLACK, opacity = 0),
                      gradient_direction[i].animate.set_fill(color = BLACK, opacity = 0),
                      grid_hog[1].animate.set_fill(color=BLACK, opacity = 0),
                      FadeOut(check_group))

        square_magnitude = gradient_magnitude[8].copy()
        number_magnitude = M_text_group[9].copy()
        square_direction = gradient_direction[8].copy()
        number_direction = alpha_text_group[9].copy()
        check_group = VGroup(square_direction, square_magnitude, number_direction, number_magnitude)
        self.play(gradient_magnitude[8].animate.set_fill(color = YELLOW, opacity = 0.5),
                    gradient_direction[8].animate.set_fill(color = YELLOW, opacity = 0.5))
        self.play(Group(square_direction, number_direction).animate.next_to(alp_text, RIGHT).scale(1.2))
        for i in range(3):
            self.play(VGroup(grid_hog[5], grid_hog[6]).animate.set_fill(color=BLACK, opacity = 0), run_time = 0.1)
            self.play(VGroup(grid_hog[5], grid_hog[6]).animate.set_fill(color=YELLOW, opacity = 0.5), run_time = 0.1)
        self.play(Group(square_magnitude, number_magnitude).animate.next_to(m_text, RIGHT).scale(1.2))
        s3 = MathTex(r"M' = \frac{M}{20} = \frac{24}{20} = 1.2", color=WHITE, font_size = 30).move_to(ORIGIN+UP*0.5)
        self.play(Write(s3))
        for i in range(2):
            self.play(grid_hog[i+5].animate.set_fill(color=PINK, opacity = 0.5))
            alpha_check = alpha_group[i+4].copy()
            s4 = Text("d = |", color=WHITE, font_size = 25).next_to(s3, DOWN*0.7).shift(LEFT*1.1)
            self.play(Write(s4))
            self.play(alpha_check.animate.next_to(s4, RIGHT*0.5).scale(1.1))
            s_dis = Text("-", color=WHITE, font_size = 25).next_to(alpha_check, RIGHT)
            self.play(Write(s_dis))
            self.play(number_direction.animate.next_to(s_dis, RIGHT))
            s_result = Text("| = 10", font="SF Pro", color=WHITE, font_size = 25).next_to(number_direction, RIGHT*0.5)
            self.play(Write(s_result))
            s5 = MathTex(f"M_{i+5} = M' * d = 1.2 * 10 = ", color=WHITE, font_size = 35).next_to(s4, DOWN*0.7).shift(RIGHT*0.9)
            self.play(Write(s5))
            text_group = VGroup(s4, alpha_check, s_dis, s_result, s5)
            s_results = Text("12", font="SF Pro", color=WHITE, font_size = 25).next_to(s5, RIGHT*0.5)
            self.play(Write(s_results))
            self.wait(1)
            self.play(s_results.animate.move_to(grid_hog[i+15].get_center()).scale(0.8))
            self.play(FadeOut(M_group[i+4]))
            M_group.remove(M_group[i+4])
            M_group.insert(i+4, s_results)
            self.play(FadeOut(text_group),
                      grid_hog[i+5].animate.set_fill(color=BLACK, opacity = 0),
                      number_direction.animate.move_to(square_direction.get_center()))
        self.play(gradient_magnitude[8].animate.set_fill(color = BLACK, opacity = 0),
                  gradient_direction[8].animate.set_fill(color = BLACK, opacity = 0),
                  FadeOut(check_group, s3, alp_text, m_text))
        self.wait(0.5)
        self.play(VGroup(grid_hog, alpha_group, M_group, hog_text).animate.move_to(ORIGIN))

        histogram_number = self.cal_histogram(image, magnitude, direction)
        histogram_number_group = VGroup()
        for i in range(9):
            histogram_number_text = Text(f"{round(histogram_number[i])}", color=WHITE, font="SF Pro", font_size=18).move_to(grid_hog[i+11].get_center())
            self.play(FadeOut(M_group[i]),
                      Write(histogram_number_text.scale(0.8)),
                      run_time = 0.2)
            histogram_number_group.add(histogram_number_text)
        self.wait(1.5)

        self.play(FadeOut(gradient_magnitude, gradient_magnitude_text, M_text_group,
                          gradient_direction, gradient_direction_text, alpha_text_group),
                          Group(grid_hog, alpha_group, hog_text, histogram_number_group).animate.move_to(ORIGIN+LEFT*3.5))
        
        center_point = grid_hog.get_edge_center(RIGHT) + RIGHT*4 + DOWN*3
        hog_illustration_group = VGroup()  
        angles = [0, 20, 40, 60, 80, 100, 120, 140, 160]
        for i, value in enumerate(histogram_number[:9]):
            angle = angles[i] * DEGREES
            length = 0.0023 * value  
            arrow = Arrow(
                start=center_point,
                end=center_point + length * np.array([np.cos(angle), np.sin(angle), 0]),
                buff=0,
                color=WHITE,
                stroke_width=2
            )
            hog_illustration_group.add(arrow)
        self.play(Create(hog_illustration_group))
        self.wait(1.5)

        self.play(FadeOut(grid_hog, alpha_group, hog_text, histogram_number_group, hog_illustration_group))
        text_original_img = Text("Original Image", font = "Segoe UI", font_size = 23).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play((FadeIn(original_image.move_to(ORIGIN + DOWN*0.5))))
        hog_img = self.create_hog_img()
        cv2.imwrite("hog_image.jpg", hog_img*255)
        hog_image = ImageMobject("hog_image.jpg").scale(1.2)
        text_hog_img = Text("HOG Image", font = "Segoe UI", font_size = 23).set_color_by_gradient(LIGHT_BROWN, PINK, GREEN)
        self.play(FadeIn(hog_image.move_to(original_image.get_center())))
        self.play(original_image.animate.move_to(LEFT*3.5 + DOWN*0.7),
                  hog_image.animate.move_to(RIGHT*3.5 + DOWN*0.7))
        self.play(Write(text_original_img.next_to(original_image, UP*1.5)),
                  Write(text_hog_img.next_to(hog_image, UP*1.2)))
        
        self.wait(5)

    def sobel(self, matrix1, matrix2):
        sum = 0
        for i in range(3):
            for j in range(3):
                sum += matrix1[i][j] * matrix2[i][j]
        return sum
    
    def direction(self, a, b):
        alpha = math.atan(b/a)
        if alpha < 0:
            alpha += math.pi
        return round(math.degrees(alpha))
    
    def create_arrow_up(self, img):
        arrow_up = DoubleArrow(
            start=img.get_corner(UL+LEFT*0.3),
            end=img.get_corner(UR+RIGHT*0.3),
            color=YELLOW,
            buff=0.1,
            stroke_width=2,    
            tip_length=0.1 
        ).shift(UP * 0.2)
        return arrow_up
    
    def create_arrow_right(self, img):
        arrow_right = DoubleArrow(
            start=img.get_corner(UR + UP*0.3),
            end=img.get_corner(DR + RIGHT*0.3),
            color=YELLOW,
            buff=0.1,
            stroke_width=2,    
            tip_length=0.1 
        ).shift(RIGHT * 0.2)
        return arrow_right
    
    def create_hog_img(self):
        image = io.imread("example.jpg")
        if image.shape[2] == 4: 
            image = image[:, :, :3]  
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hog_features, hog_image = hog(image_gray, 
                                    orientations=8, 
                                    pixels_per_cell=(16, 16), 
                                    cells_per_block=(1, 1), 
                                    block_norm='L2-Hys', 
                                    visualize=True)

        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
        return hog_image_rescaled
    
    def cell_histogram(self, cell_magnitude, cell_direction):
        histogram = np.zeros(9)
        for i in range(cell_magnitude.shape[0]):
            for j in range(cell_magnitude.shape[1]):
                mag = cell_magnitude[i][j]
                angle = cell_direction[i][j]
                bin_idx = int(angle / 20) % 9
                histogram[bin_idx] += mag
        return histogram
    
    def cal_histogram(self, image, magnitude, direction):
        hog_features = []
        cell_size = (8, 8)
        for i in range(0, image.shape[0], cell_size[0]):
            for j in range(0, image.shape[1], cell_size[1]):
                cell_magnitude = magnitude[i:i+cell_size[0], j:j+cell_size[1]]
                cell_direction = direction[i:i+cell_size[0], j:j+cell_size[1]]
                cell_hist = self.cell_histogram(cell_magnitude, cell_direction)
                hog_features.extend(cell_hist)
        hog_features = np.array(hog_features)
        return hog_features