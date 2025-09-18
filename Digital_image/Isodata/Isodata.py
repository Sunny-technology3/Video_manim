from manim import *
import cv2
import numpy
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

class Isodata(Scene):
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

        txt_header = Text("Phân vùng ảnh theo ngưỡng biên độ", 
                          font= "JetBrains Mono", font_size= 38).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).move_to(ORIGIN)
        self.play(Write(txt_header.shift(UP)))
        txt_header1 = Text("Thuật toán đẳng liệu",
                           font= "JetBrains Mono", font_size= 38).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN).next_to(txt_header, DOWN)
        self.play(Succession(Write(txt_header1),
                             ApplyWave(Group(txt_header, txt_header1), scale_factor = 1.2),
                             Group(txt_header, txt_header1).animate.move_to(UP*3.3).scale(0.65)))
    
    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        img = cv2.imread("example.jpg")
        original_image = ImageMobject("example.jpg").scale(2.5).move_to(ORIGIN+DOWN*0.5)
        original_text_img = Text("Original Image", font= "Segoe UI", font_size= 22).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(FadeIn(original_image))
        self.play(Succession(Write(original_text_img.next_to(original_image, UP)),
                             Group(original_image, original_text_img).animate.shift(LEFT * 2.5)))

        red_overlay = Rectangle(width=2 * 0.1, height=2 * 0.1, color=RED, fill_opacity=0)
        overlay_x = 16 * 0.1  
        overlay_y = 12.5 * 0.1  
        red_overlay.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        cropped_img = img[50:60, 50:60]
        cv2.imwrite("cropped_img.jpg", cropped_img)
        cropped_image = ImageMobject("cropped_img.jpg").move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(cropped_image.animate.next_to(original_image, RIGHT*12).scale(50), run_time = 0.5)
        
        y_values = [2, 4, 3, 5, 3, 1, 5, 4, 2, 3]
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            axis_config={"color": WHITE},
            y_length=10,
            x_length=9,
            x_axis_config={
                "numbers_to_include": range(0, 9, 1),
                "tick_size": 0.05,  
            },
            y_axis_config={
                "numbers_to_include": range(0, 6, 1),
                "tick_size": 0.05,
            }
        ).add_coordinates().scale(0.4).move_to(cropped_image)
        
        x_label_0 = Text("0", font= "Segoe UI", font_size=11).next_to(axes.c2p(0, 0), DOWN, buff=0.1)
        x_label = Text("r", font_size=18, color = WHITE).next_to(axes.c2p(9.8, 0), DOWN*0.5, buff=0.3)  
        y_label = MathTex(r"p(r_k)", font_size=25, color = WHITE).next_to(axes.c2p(0, 5.9), LEFT*0.5, buff=0.3) 

        stems = VGroup()
        for x, y in zip(range(10), y_values):
            line = Line(axes.c2p(x, 0), axes.c2p(x, y), color=BLUE)         
            stems.add(line)

        axes_group = VGroup(axes, stems, x_label, y_label, x_label_0)
        self.play(FadeOut(cropped_image, run_time = 0.3))
        self.play(FadeIn(axes_group))
        self.wait(1)
        self.play(FadeOut(original_image, original_text_img, red_overlay),
                  axes_group.animate.move_to(LEFT*4.5))

        text_group = VGroup()
        a1 = 5.5
        text1 = MathTex(r"Give: T_0 = 5.5, \epsilon = 0.25, \Delta T = \infty ", font_size=30).next_to(axes_group, RIGHT*3).shift(UP*2.3)
        text_group.add(text1)
        self.play(Write(text1))
        line_check1 = Line(axes.c2p(a1, 0), axes.c2p(a1, 5.5), color=RED)
        x_label_check1 = Text(f"{a1}", font= "Segoe UI", color=RED, font_size=11).next_to(axes.c2p(a1, 0), DOWN, buff=0.1)
        self.play(Create(line_check1), Write(x_label_check1))

        text_g1 = MathTex(r"G_1 (r_k > 5.5):", font_size=30).next_to(text1, DOWN).shift(LEFT)
        self.play(Write(text_g1))
        line_group_check1 = VGroup(stems[6:10])
        self.play(line_group_check1.animate.set_color(YELLOW))
        text_m1 = MathTex(r"m_1 = \frac{\sum_{i=6}^9 r_ip(r_i)}{\sum_{i=6}^9 p(r_i)} = \frac{6.5 + 7.4 + 8.2 + 9.3}{5 + 4 + 2 + 3} = 7.214",
                        font_size=25).next_to(text_g1, DOWN).shift(RIGHT*2.3)
        self.play(Write(text_m1))
        self.play(line_group_check1.animate.set_color(BLUE))
        text_g2 = MathTex(r"G_2 (r_k \leq 5.5):", font_size=30).next_to(text_g1, DOWN*5)
        self.play(Write(text_g2))
        line_group_check2 = VGroup(stems[0:6])
        self.play(line_group_check2.animate.set_color(YELLOW))
        text_m2 = MathTex(r"m_2 = \frac{\sum_{i=0}^5 r_ip(r_i)}{\sum_{i=0}^5 p(r_i)} = \frac{0.2 + 1.4 + 2.3 + 3.5 + 4.3 + 5.1}{2 + 4 + 3 + 5 + 3 + 1} = 2.333",
                        font_size=25).next_to(text_g2, DOWN).shift(RIGHT*3)
        self.play(Write(text_m2))
        self.play(line_group_check2.animate.set_color(BLUE))
        text_result = MathTex(r"\implies T_1 = \frac{1}{2} (m_1 + m_2) = 4.774", 
                              font_size=25).next_to(text_m2, DOWN*1.5).shift(LEFT*1.7)
        self.play(Write(text_result))
        text_result1 = MathTex(r"\implies \Delta T = \lvert T_0 - T_1 \rvert = \lvert 5.5 - 4.774 \rvert = 0.726", 
                              font_size=25).next_to(text_result, DOWN).shift(RIGHT*0.65)
        self.play(Write(text_result1))
        text_result2 = MathTex(r"\implies \Delta T > \epsilon \implies", 
                              font_size=25).next_to(text_result1, DOWN).shift(LEFT*1.5)
        self.play(Write(text_result2))
        text_continue = Text("Continue", font= "Segoe UI", font_size= 25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Succession(Write(text_continue.next_to(text_result2, RIGHT)),
                             Indicate(text_continue, color=PURPLE)))
        self.play(FadeOut(text_g1, text_g2, text_m1, text_m2, text_result, text_result1, text_result2, text_continue))

        a2 = 4.774
        text2 = MathTex(r"T_1 = 4.774", font_size=30).next_to(text1, DOWN).shift(LEFT*0.8)
        text_group.add(text2)
        self.play(Write(text2))
        line_check2 = Line(axes.c2p(a2, 0), axes.c2p(a2, 5.5), color=RED)
        x_label_check2 = Text(f"{a2}", font= "Segoe UI", color=RED, font_size=11).next_to(axes.c2p(a2, 0), DOWN*2.5, buff=0.1)
        self.play(Transform(line_check1, line_check2),
                  Transform(x_label_check1, x_label_check2))
        axes_group.add(line_check2, x_label_check2, line_check1, x_label_check1)
        
        text_g21 = MathTex(r"G_1 (r_k > 4.774):", font_size=30).next_to(text1, DOWN*3).shift(LEFT*1.1)
        text_group.add(text_g21)
        self.play(Write(text_g21))
        line_group_check21 = VGroup(stems[5:10])
        self.play(line_group_check21.animate.set_color(YELLOW))
        text_m21 = MathTex(r"m_1 = \frac{\sum_{i=5}^9 r_ip(r_i)}{\sum_{i=5}^9 p(r_i)} = \frac{5.1 + 6.5 + 7.4 + 8.2 + 9.3}{1 + 5 + 4 + 2 + 3} = 7.061",
                        font_size=25).next_to(text_g21, DOWN).shift(RIGHT*2.5)
        text_group.add(text_m21)
        self.play(Write(text_m21))
        self.play(line_group_check21.animate.set_color(BLUE))
        text_g22 = MathTex(r"G_2 (r_k \leq 4.774):", font_size=30).next_to(text_g21, DOWN*5)
        text_group.add(text_g22)
        self.play(Write(text_g22))
        line_group_check22 = VGroup(stems[0:5])
        self.play(line_group_check22.animate.set_color(YELLOW))
        text_m22 = MathTex(r"m_2 = \frac{\sum_{i=0}^4 r_ip(r_i)}{\sum_{i=0}^4 p(r_i)} = \frac{0.2 + 1.4 + 2.3 + 3.5 + 4.3}{2 + 4 + 3 + 5 + 3} = 2.176",
                        font_size=25).next_to(text_g22, DOWN).shift(RIGHT*2.5)
        text_group.add(text_m22)
        self.play(Write(text_m22))
        self.play(line_group_check22.animate.set_color(BLUE))
        text_result23 = MathTex(r"\implies T_2 = \frac{1}{2} (m_1 + m_2) = 4.619", 
                              font_size=25).next_to(text_m22, DOWN*1.5).shift(LEFT*1.5)
        self.play(Write(text_result23))
        text_result21 = MathTex(r"\implies \Delta T = \lvert T_1 - T_2 \rvert = \lvert 4.774 - 4.619 \rvert = 0.155", 
                              font_size=25).next_to(text_result23, DOWN).shift(RIGHT*0.9)
        self.play(Write(text_result21))
        text_result22 = MathTex(r"\implies \Delta T < \epsilon \implies", 
                              font_size=25).next_to(text_result21, DOWN).shift(LEFT*1.6)
        self.play(Write(text_result22))
        text_group.add(text_result21, text_result22, text_result23)
        text_end = Text("End", font= "Segoe UI", font_size= 25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(Succession(Write(text_end.next_to(text_result22, RIGHT)),
                             Indicate(text_end, color=PURPLE)))
        
        text_results = Text("Ngưỡng toàn cục : T = 5 ( Làm tròn 4.774)", color = RED, font= "Segoe UI", font_size= 19)
        self.play(Write(text_results.next_to(axes, DOWN*1.5).shift(RIGHT*0.1)))
        self.wait(1)
        self.play(FadeOut(axes_group, text_group, text_end, text_results))

        image = cv2.imread("example.jpg", cv2.IMREAD_GRAYSCALE)
        ret, otsu_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite("isodata_result.jpg", otsu_image)

        isodata_image = ImageMobject("isodata_result.jpg").scale(3.12)
        self.play(FadeIn(original_image.move_to(ORIGIN + DOWN*0.5).scale(1.25)))
        self.play(FadeIn(isodata_image.move_to(original_image.get_center())),  lag_ratio=0.1, run_time = 1)
        text_original = Text("Original Image", font="SF Pro", font_size=25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        text_isodata = Text("Isodata Image", font="SF Pro", font_size=25).set_color_by_gradient(PURE_BLUE, PURE_GREEN, GREEN)
        self.play(original_image.animate.move_to(LEFT*3.2+DOWN*0.5), isodata_image.animate.move_to(RIGHT*3.2+DOWN*0.5))
        self.play(Write(text_original.next_to(original_image, UP)), Write(text_isodata.next_to(isodata_image, UP)))

        self.wait(5)