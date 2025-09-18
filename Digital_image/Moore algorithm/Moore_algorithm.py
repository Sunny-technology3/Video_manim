from manim import *
import cv2
import numpy
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class MooreAlgorithm(Scene):
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

        txt_header = Text("Phát hiện biên theo quy hoạch động", 
                          font= "JetBrains Mono", font_size= 38).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).move_to(ORIGIN)
        self.play(Write(txt_header.shift(UP)))
        txt_header1 = Text("Thuật toán dò biên sử dụng cặp điểm nền-vùng",
                           font= "JetBrains Mono", font_size= 38).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).next_to(txt_header, DOWN)
        self.play(Succession(Write(txt_header1),
                             ApplyWave(Group(txt_header, txt_header1), scale_factor = 1.2),
                             Group(txt_header, txt_header1).animate.move_to(UP*3.3).scale(0.65)))
    
    def moore_boundary(self, binary_image):
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        height, width = binary_image.shape

        boundary = []
        start = None
        for i in range(height):
            for j in range(width):
                if binary_image[i, j] == 1:
                    start = (i, j)
                    break
            if start:
                break
        if not start:
            return boundary  
        
        current = start
        boundary.append(current)
        prev_direction = 0
        while True:
            found = False
            for step in range(8):
                direction_idx = (prev_direction + step) % 8
                ni, nj = current[0] + directions[direction_idx][0], current[1] + directions[direction_idx][1]
                if 0 <= ni < height and 0 <= nj < width and binary_image[ni, nj] == 1:
                    current = (ni, nj)
                    boundary.append(current)
                    prev_direction = (direction_idx + 5) % 8 
                    found = True
                    break
            if not found or current == start:
                break

        return boundary
    
    def create_line(self):
        line_group = VGroup()
        directions = [
            (UP, DOWN),         
            (RIGHT, LEFT),      
            (UR, DL),          
            (UL, DR),           
            (UP + LEFT, DOWN + RIGHT),  
            (UP + RIGHT, DOWN + LEFT)]
        
        for start_dir, end_dir in directions:
            line = DoubleArrow(start_dir * 3, end_dir * 3, color=RED,
                                stroke_width=4, tip_length=0.5)
            line_group.add(line)
        return line_group
    
    def create_arc(self, center, radius, start_angle, angle, num_dashes, rotate_angle):
        arc = Arc(
            radius=radius,
            start_angle=start_angle,
            angle=angle,
            color=BLUE,
            stroke_width=3
        ).move_to(center+UP*0.1+LEFT*0.1)
        dashed_arc = DashedVMobject(arc, num_dashes=num_dashes)
        arrow_tip = Triangle(color=BLUE).scale(0.08).rotate(rotate_angle)
        arrow_tip.move_to(arc.point_from_proportion(1))
        arrow_arc = VGroup(dashed_arc, arrow_tip)
        return arrow_arc
            
    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        matrix = np.array([[0, 0, 0, 0, 0, 0, 0, 0], 
                           [0, 0, 1, 1, 1, 1, 0, 0], 
                           [0, 1, 1, 1, 1, 1, 1, 0],
                           [0, 1, 1, 1, 1, 1, 1, 0], 
                           [0, 0, 0, 1, 1, 1, 1, 0], 
                           [0, 0, 0, 0, 1, 1, 0, 0], 
                           [0, 0, 0, 0, 0, 0, 0, 0]])
        grid = VGroup()
        square_check_group = VGroup()
        check = False
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(WHITE, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=WHITE, font="SF Pro", font_size=18).move_to(square.get_center())
                grid.add(VGroup(square, number))
                if check == False and matrix[i][j] == 0:
                    square_check_group.add(square)
                else:
                    check = True
        grid.move_to(ORIGIN).shift(DOWN*0.8).scale(1.25)
        self.play(FadeIn(grid))
        text_matrix = Text("Input Matrix", font = "Segoe UI", font_size= 30).next_to(grid, UP*2).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Write(text_matrix))
        
        for square in square_check_group:
            self.play(square.animate.set_fill(color=YELLOW, opacity=0.5), run_time = 0.1)
            self.play(square.animate.set_fill(color=RED, opacity=0.5), run_time = 0.1)
        
        for i in range(3):
            self.play(grid[10][0].animate.set_fill(color=BLACK, opacity=0),
                      grid[10][0].animate.set_fill(color=YELLOW, opacity=0.5), run_time = 0.2)
            self.play(grid[10][0].animate.set_fill(color=BLACK, opacity=0.5),
                      grid[10][0].animate.set_fill(color=GREEN_C, opacity=0.5), run_time = 0.2)
        self.play(square_check_group.animate.set_fill(color=BLACK, opacity=0))
        
        text_group = VGroup()
        number_group = VGroup()
        square_group_yellow = VGroup()
        for i in range(3):
            text_b = MathTex(f"b_{i}", color = WHITE, font_size = 25)
            text_group.add(text_b)
            self.play(Succession(grid[10+i][1].animate.shift(LEFT*0.15),
                                 FadeIn(text_b.next_to(grid[10+i][1], RIGHT*0.01).shift(LEFT*0.06))))
            number_group.add(grid[10+i][1])
            line1 = Arrow(start = grid[10+i][1].get_bottom(), end = grid[9+i][1].get_bottom(), color = RED)
            text_c = MathTex(f"c_{i}", color = WHITE, font_size = 25)
            text_group.add(text_c)
            if i == 0:
                self.play(Create(line1))
                self.play(grid[9+i][0].animate.set_fill(color=BLACK, opacity=0),
                          grid[9+i][0].animate.set_fill(color=YELLOW_C, opacity=0.5))
                square_group_yellow.add(grid[9+i][0])
                self.play(Succession(grid[9+i][1].animate.shift(LEFT*0.15),
                                     FadeIn(text_c.next_to(grid[9+i][1], RIGHT*0.005).shift(LEFT*0.06))))
                number_group.add(grid[9+i][1])
            else:
                self.play(grid[2+i][0].animate.set_fill(color=BLACK, opacity=0),
                          grid[2+i][0].animate.set_fill(color=YELLOW_C, opacity=0.5))
                square_group_yellow.add(grid[2+i][0])
                self.play(Succession(grid[2+i][1].animate.shift(LEFT*0.15),
                                     FadeIn(text_c.next_to(grid[2+i][1], RIGHT*0.005).shift(LEFT*0.06))))
                number_group.add(grid[2+i][1])
            
            line = self.create_line()
            self.play(FadeIn(line.move_to(grid[10+i].get_center()).scale(0.25)))
            if i == 0:
                arrow_arc = self.create_arc(grid[10+i].get_center(), 0.6, 17*PI/20, -7*PI/10, 15, -3*PI/2).shift(RIGHT*0.1 + UP*0.3)
            else:
                arrow_arc = self.create_arc(grid[10+i].get_center(), 0.35, PI/2, -9*PI/20, 8, -3*PI/2).shift(UP*0.35 + RIGHT*0.53)
            self.play(Create(arrow_arc))
            
            square_group_red = VGroup()
            if i == 0:
                for j in range(3):
                    square_group_red.add(grid[1+j][0])
                    self.play(grid[1+j][0].animate.set_fill(color=BLACK, opacity=0),
                              grid[1+j][0].animate.set_fill(color=RED_C, opacity=0.5))
            else:
                square_group_red.add(grid[3+i][0])
                self.play(grid[3+i][0].animate.set_fill(color=BLACK, opacity=0),
                            grid[3+i][0].animate.set_fill(color=RED_C, opacity=0.5))
            for j in range(3):    
                self.play(grid[11+i][0].animate.set_fill(color=BLACK, opacity=0), run_time = 0.2)
                self.play(grid[11+i][0].animate.set_fill(color=BLACK, opacity=0),
                          grid[11+i][0].animate.set_fill(color=GREEN_C, opacity=0.5), run_time = 0.2)
            if i == 0:
                self.play(square_group_red.animate.set_fill(color=BLACK, opacity=0),
                          FadeOut(line1, line, arrow_arc),
                          run_time = 0.5)
            else:
                self.play(square_group_red.animate.set_fill(color=BLACK, opacity=0),
                          FadeOut(line, arrow_arc),
                          run_time = 0.5)

        grid_check_b = VGroup(grid[13], grid[22], grid[30], grid[38], grid[45], grid[44], grid[35], grid[26], grid[25], grid[17])
        grid_check_c = VGroup(grid[5], grid[14], grid[31], grid[39], grid[46], grid[52], grid[43], grid[34], grid[33], grid[16])

        for i in range(len(grid_check_b)):
            x = i+4
            text_b = MathTex(r"b_{\text{" + str(x) + "}}", color = WHITE, font_size = 25)
            text_group.add(text_b)
            self.play(Succession(grid_check_b[i][1].animate.shift(LEFT*0.15),
                                 FadeIn(text_b.next_to(grid_check_b[i][1], RIGHT*0.005).shift(LEFT*0.06)),
                                 run_time = 0.2))
            number_group.add(grid_check_b[i][1])
            self.play(grid_check_c[i][0].animate.set_fill(color=BLACK, opacity=0),
                      grid_check_c[i][0].animate.set_fill(color=YELLOW_C, opacity=0.5), run_time = 0.2)
            square_group_yellow.add(grid_check_c[i][0])
            text_c = MathTex(r"c_{\text{" + str(x) + "}}", color = WHITE, font_size = 25)
            text_group.add(text_c)
            self.play(Succession(grid_check_c[i][1].animate.shift(LEFT*0.15),
                                 FadeIn(text_c.next_to(grid_check_c[i][1], RIGHT*0.005).shift(LEFT*0.06)),
                                 run_time = 0.2))
            number_group.add(grid_check_c[i][1])
            if i != len(grid_check_b)-1:
                self.play(grid_check_b[i+1][0].animate.set_fill(color=BLACK, opacity=0),
                          grid_check_b[i+1][0].animate.set_fill(color=GREEN_C, opacity=0.5), run_time = 0.2)
        self.wait(1)
        self.play(square_group_yellow.animate.set_fill(color=BLACK, opacity=0),
                  number_group.animate.shift(RIGHT*0.15),
                  FadeOut(text_group), run_time = 0.4)
        self.wait(2)

        self.play(FadeOut(grid, text_matrix))
        img = ImageMobject("example.jpg").scale(1.15).move_to(ORIGIN).shift(DOWN*0.5)
        self.play(FadeIn(img))

        image = cv2.imread("example.jpg", 0)  
        _, binary_image = cv2.threshold(image, 127, 1, cv2.THRESH_BINARY) 
        boundary_points = self.moore_boundary(binary_image)
        output_image = Image.new("RGB", (binary_image.shape[1], binary_image.shape[0]), "white")
        draw = ImageDraw.Draw(output_image)
        for idx in range(len(boundary_points) - 1):
            x1, y1 = boundary_points[idx][1], boundary_points[idx][0]
            x2, y2 = boundary_points[idx + 1][1], boundary_points[idx + 1][0]
            draw.line((x1, y1, x2, y2), fill="red", width=1)
        output_image.save("detected_boundary.jpg")
        img_mobject = ImageMobject("detected_boundary.jpg").scale(1.15)

        self.play(FadeIn(img_mobject.move_to(img.get_center())),  lag_ratio=0.1, run_time = 1)
        text1 = Text("Original Image", font="SF Pro", font_size=25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        text2 = Text("Moore Image", font="SF Pro", font_size=25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(img.animate.move_to(LEFT*3.2+DOWN*0.5), img_mobject.animate.move_to(RIGHT*3.2+DOWN*0.5))
        self.play(Write(text1.next_to(img, UP)), Write(text2.next_to(img_mobject, UP))) 
        
        self.wait(5)