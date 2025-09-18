from manim import *
import sympy as sp

def doc(a):
    with open(f"{a}", "r", encoding = "utf-8") as lf:
        lines = lf.readlines()   
    return lines

class DrawLine(Scene):
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

    def construct(self):
        self.camera.background_color = WHITE
        self.camera.background_opacity = 0.5
        self.logo()

        lst = doc("FFT_time.txt")

        title = Text("Fast Fourier Transform" , color = BLACK, font_size = 55).move_to(ORIGIN)
        self.play(Write(title))
        title1 = Text("Decimation In Time" , color = BLACK, font_size = 40).move_to(ORIGIN+DOWN*0.7)
        self.play(Succession(Write(title1), Indicate(Group(title, title1), color = RED, scale_factor = 1.2),
                             VGroup(title, title1).animate.move_to(UP*3).scale(0.7)))
        self.wait(1)

        dot1 = VGroup(*[Dot(5*LEFT + (i-1)*DOWN, color = BLACK) for i in range(4)])
        dot2 = VGroup(*[Dot(4*LEFT + (i-1)*DOWN, color = BLACK) for i in range(4)])
        dot3 = VGroup(*[Dot(LEFT + (i-1)*DOWN, color = BLACK) for i in range(4)])
        dot4 = VGroup(*[Dot(RIGHT + (i-1)*DOWN, color = BLACK) for i in range(4)])
        dot5 = VGroup(*[Dot(4*RIGHT + (i-1)*DOWN, color = BLACK) for i in range(4)])
        self.add(dot1, dot2, dot3, dot4, dot5)

        line1 = VGroup(*[Line(dot_1, dot_2, color = BLACK, stroke_width=7) for dot_1, dot_2 in zip(dot1, dot2)])
        line2 = VGroup(*[Line(dot_1, dot_2, color = BLACK, stroke_width=7) for dot_1, dot_2 in zip(dot2, dot3)])
        line3 = VGroup(*[Line(dot_1, dot_2, color = BLACK, stroke_width=7) for dot_1, dot_2 in zip(dot3, dot4)])
        line4 = VGroup(*[Line(dot_1, dot_2, color = BLACK, stroke_width=7) for dot_1, dot_2 in zip(dot4, dot5)])
        line5 = VGroup(*[Line(dot_1, Dot(5*RIGHT + (i-1)*DOWN), color = BLACK, stroke_width=8) for dot_1, i in zip(dot5, range(4))])
        self.add(line1, line2, line3, line4, line5)

        line_text1 = VGroup(*[Text(f"x({i}) = ", font= "Segoe UI", color = BLACK).next_to(line, LEFT).scale(0.5) for i, line in zip(range(0, 3, 2), line1)])
        self.add(line_text1)
        for i in range(2):
            line_text2 = Text(f"x({2*i + 1}) = ", font= "Segoe UI", color = BLACK).next_to(line1[i+2], LEFT).scale(0.5)
            self.add(line_text2)

        arrow1 = VGroup(*[Arrow(start = Dot(5*LEFT + DOWN * (i-1)), end =  (4*LEFT + DOWN*(i-1)), buff = 0, color = BLACK).scale(0.5) for i in range(4)])
        arrow2 = VGroup(*[Arrow(start = Dot(2*LEFT + DOWN * (i-1)), end =  (LEFT + DOWN*(i-1)), buff = 0, color = BLACK).scale(0.5) for i in range(4)])
        arrow3 = VGroup(*[Arrow(start = Dot(0.5*LEFT + DOWN * (i-1)), end =  (0.5*RIGHT + DOWN*(i-1)), buff = 0, color = BLACK).scale(0.5) for i in range(4)])
        arrow4 = VGroup(*[Arrow(start = Dot(3*RIGHT + DOWN * (i-1)), end =  (4*RIGHT + DOWN*(i-1)), buff = 0, color = BLACK).scale(0.5) for i in range(4)])
        arrow5 = VGroup(*[Arrow(start = Dot(4*RIGHT + DOWN * (i-1)), end =  (5*RIGHT + DOWN*(i-1)), buff = 0, color = BLACK).scale(0.5) for i in range(4)])
        self.add(arrow1, arrow2, arrow3, arrow4, arrow5 )

        line6 = VGroup()
        for i in range(4):
            if i%2 == 0:
                line = Line(dot2[i], dot3[i+1], color = BLACK, stroke_width=7).add_tip(tip_length=0.1)
            else:
                line = Line(dot2[i], dot3[i-1], color = BLACK, stroke_width=7).add_tip(tip_length=0.1)
            line6.add(line)
            self.add(line)

        line7 = VGroup()
        for i in range(4):
            if i<2:
                line = Line(dot4[i], dot5[i+2], color = BLACK, stroke_width=7).add_tip(tip_length=0.1)
            else:
                line = Line(dot4[i], dot5[i-2], color = BLACK, stroke_width=7).add_tip(tip_length=0.1)
            line7.add(line)
            self.add(line)

        text = VGroup()
        text1 = Text("-1", font= "Segoe UI", color = BLACK, font_size = 30).next_to(arrow2[1], DOWN/3)
        text2 = Text("-1", font= "Segoe UI", color = BLACK, font_size = 30).next_to(arrow2[3], DOWN/3)
        text3 = Text("-1", font= "Segoe UI", color = BLACK, font_size = 30).next_to(arrow4[2], DOWN/3)
        text4 = Text("-1", font= "Segoe UI", color = BLACK, font_size = 30).next_to(arrow4[3], DOWN/3)
        text.add(text1, text2, text3, text4)
        self.add(text1, text2, text3, text4)

        j = sp.symbols('j')
        lst_num3 = [1, 1, 1, -j]
        text_1 = MathTex("W_4^0 = 1", color = BLACK, font_size = 30).next_to(arrow1[1], DOWN/3)
        text_2 = MathTex("W_4^0 = 1", color = BLACK, font_size = 30).next_to(arrow1[3], DOWN/3)
        text_3 = MathTex("W_4^0 = 1", color = BLACK, font_size = 30).next_to(arrow3[2], DOWN/3)
        text_4 = MathTex("W_4^1 = -j", color = BLACK, font_size = 30).next_to(arrow3[3], DOWN/3)
        self.add(text_1, text_2, text_3, text_4)

        lst_num = []
        for i in range(4):
            lst_num.append(lst[i])
        num_text = VGroup(*[Text(str(num), font= "Segoe UI", color = BLACK).next_to(line, LEFT).scale(0.5) for num, line in zip(lst_num, line1)])
        self.play(Write(num_text), run_time = 3)    

        lst_num1 = []
        for i in range(4):
            if i %2 == 0:
                line_group1 = Group(line1[i], arrow1[i], dot1[i], line2[i], arrow2[i], dot2[i], dot3[i])
                line_group2 = Group(line1[i+1], arrow1[i+1], dot1[i+1], dot2[i+1], line6[i + 1])
                self.play(line_group1.animate.set_color(RED))
                self.play(line_group2.animate.set_color(RED))
                s = MathTex(f"{lst_num[i]} + {lst_num[i+1]}", color = BLACK, font_size = 25).next_to(dot3[i], UP)
                num = int(lst_num[i]) + int(lst_num[i+1])
                lst_num1.append(num)
                self.play(FadeOut(s), run_time = 3)
                s1 = Text(str(num), font= "Segoe UI", color = BLACK, font_size = 30).next_to(dot3[i], UP)
                self.play(FadeIn(s1))
                self.play(line_group1.animate.set_color(BLACK))
                self.play(line_group2.animate.set_color(BLACK))
            else:
                line_group1 = Group(line1[i-1], arrow1[i-1], dot1[i-1], dot2[i-1], line6[i-1], dot3[i])
                line_group2 = Group(line1[i], arrow1[i], dot1[i], line2[i], arrow2[i], dot2[i], text[int(i/2)])
                self.play(line_group1.animate.set_color(RED))
                self.play(line_group2.animate.set_color(RED))
                s = MathTex(f"{lst_num[i-1]} + {lst_num[i]}.(-1)", color = BLACK, font_size = 25).next_to(dot3[i], UP)
                num = int(lst_num[i-1]) - int(lst_num[i])
                lst_num1.append(num)
                self.play(FadeOut(s), run_time = 3)
                s1 = Text(str(num), font= "Segoe UI", color = BLACK, font_size = 30).next_to(dot3[i], UP)
                self.play(FadeIn(s1))
                self.play(line_group1.animate.set_color(BLACK))
                self.play(line_group2.animate.set_color(BLACK))

        lst_num2 = []
        for i in range(4):
            if i < 2:
                line_group1 = Group(line3[i], arrow3[i], dot5[i], dot3[i], line4[i], arrow4[i], dot4[i])
                line_group2 = Group(line3[i+2], arrow3[i+2], dot3[i+2], dot4[i+2], line7[i + 2])
                self.play(line_group1.animate.set_color(RED))
                self.play(line_group2.animate.set_color(RED))
                if i %2 == 0:
                    s = Text(f"{lst_num1[i]} + {lst_num1[i+2]}", font= "Segoe UI", color = BLACK, font_size = 25).next_to(dot5[i], RIGHT + UP)
                    num = int(lst_num1[i]) + int(lst_num1[i+2])
                    lst_num2.append(num)
                    self.play(FadeOut(s), run_time = 3) 
                else:
                    s = Text(f"{lst_num1[i]} + {lst_num1[i+2]} . {lst_num3[3]}", font= "Segoe UI", color = BLACK, font_size = 25).next_to(dot5[i], RIGHT*0.5 + UP)
                    expr = lst_num1[i] + lst_num1[i+2] * lst_num3[i+2]
                    num = sp.simplify(expr)
                    lst_num2.append(num)                     
                    self.play(FadeOut(s), run_time = 3)
                s1 = Text(str(lst_num2[i]), font= "Segoe UI", color = BLACK, font_size = 30).next_to(dot5[i], RIGHT + UP)
                self.play(FadeIn(s1))
                self.play(line_group1.animate.set_color(BLACK))
                self.play(line_group2.animate.set_color(BLACK))
            else:
                line_group1 = Group(line3[i-2], arrow3[i-2], dot3[i-2], dot5[i], dot4[i-2], line7[i-2])
                line_group2 = Group(line3[i], arrow3[i], dot3[i], line4[i], arrow4[i], dot4[i], text[i])
                self.play(line_group1.animate.set_color(RED))
                self.play(line_group2.animate.set_color(RED))
                if i %2 == 0:
                    s = Text(f"{lst_num1[i-2]} + {lst_num1[i]}.(-1)", font= "Segoe UI", color = BLACK, font_size = 25).next_to(dot5[i], RIGHT + UP)
                    num = int(lst_num1[i-2]) - int(lst_num1[i])
                    lst_num2.append(num)
                    self.play(FadeOut(s), run_time = 3) 
                else:
                    s = Text(f"{lst_num1[i-2]} + {lst_num1[i]} . {lst_num3[3]}", font= "Segoe UI", color = BLACK, font_size = 25).next_to(dot5[i], RIGHT*0.5 + UP)
                    expr = lst_num1[i-2] + lst_num1[i] * lst_num3[i] * (-1)
                    num = sp.simplify(expr)
                    lst_num2.append(num)                     
                    self.play(FadeOut(s), run_time = 3)
                s1 = Text(str(num), font= "Segoe UI", color = BLACK, font_size = 30).next_to(dot5[i], RIGHT + UP)
                self.play(FadeIn(s1))
                self.play(line_group1.animate.set_color(BLACK))
                self.play(line_group2.animate.set_color(BLACK))
            line_group3 = Group(line5[i], arrow5[i])
            self.play(line_group3.animate.set_color(RED))
            line_text2 = Text(f"X({i}) = {num}", font= "Segoe UI", color = BLACK).move_to(6*RIGHT + DOWN * (i-1)).scale(0.5)
            self.play(Write(line_text2))
            self.play(line_group3.animate.set_color(BLACK))

        lst_kq = VGroup(*[Text(f"X({i}) = {num}", font= "Segoe UI", color = BLACK, font_size = 30) for i, num in zip(range(4), lst_num2)])
        for i in range(4):
            self.play(Write(lst_kq[i].move_to(DOWN * 3 + RIGHT * 2.5 * (i - 1.5))))
            
        self.wait(5)