from manim import *

def doc(a):
    with open(f"{a}", "r", encoding = "utf-8") as lf:
        lines = lf.read().split()   
    return lines

class BinarySearch(Scene):
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
                        ).scale(0.5).to_edge(DR).shift(DOWN * 0.35, RIGHT * 0.35)
        txt_intro.set_color(ORANGE)
        self.play(Write(txt_intro), run_time = 1.5)

    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        a2 = Text("BinarySearch", font= "Segoe UI", color = WHITE, font_size=50).move_to(ORIGIN)
        self.play(Succession(Write(a2), Indicate(a2, scale_factor = 1.2),a2.animate.to_edge(UP).scale(0.7)))

        numbers = doc("binarysearch.txt")
        x = 1
        target_number = numbers[len(numbers) - 1]
        target_index = numbers.index(target_number)
        target_text = Text(f"Find: {target_number}", font="Comic Sans MS", color = WHITE, font_size=40).next_to(a2, DOWN)
        self.play(Write(target_text))

        squares = VGroup(*[Square(side_length=1, color=WHITE).shift(RIGHT * i) for i in range(len(numbers) - 1)])
        self.add(squares)

        number_texts = VGroup(*[Text(str(num), color = WHITE).move_to(square.get_center()) for num, square in zip(numbers, squares)])
        self.add(number_texts)

        squares_check = Square(side_length=1, color = WHITE)
        target_number_check = Text(str(target_number), color = WHITE).move_to(squares_check.get_center())
        squares_group_check = Group(squares_check, target_number_check)

        squares_group1 = Group(squares, number_texts)           
        squares_group1.move_to(DOWN*2.5 + ORIGIN)

        l = 0
        r = len(numbers) - 2
        y = 1
        while l<=r:
            x = int((l+r)/2)
            a = Text("LEFT", color=WHITE, font_size = 25).move_to(UP*2 + LEFT*2)
            self.play(Write(a))
            for j in range(3):
                    self.play(squares[l].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                    self.play(squares[l].animate.set_fill(WHITE, opacity=0), run_time = 0.35)
            b = Text("RIGHT", color=WHITE, font_size = 25).next_to(a, DOWN)
            self.play(Write(b))
            for j in range(3):
                    self.play(squares[r].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                    self.play(squares[r].animate.set_fill(WHITE, opacity=0), run_time = 0.35)
            fractions = MathTex(r"MID = \frac{LEFT + RIGHT}{2}", color=WHITE, font_size = 30, opacity = 1).next_to(b, RIGHT * 2)
            self.play(Write(fractions))
            squares_group = Group(squares[x], number_texts[x])
            self.play(squares[x].animate.set_fill(YELLOW, opacity=0.5))
            squares_group.next_to(squares[x], UP)
            self.play(FadeIn(squares_group_check.next_to(squares_group, UP*2.5)))
            if numbers[x] == target_number:
                z = Text("≠", color = WHITE, font_size = 40).next_to(squares_group, UP*0.8)
                self.play(Write(z))
                for j in range(3):
                    self.play(squares[x].animate.set_fill(GREEN, opacity=0.5), run_time = 0.35)
                    self.play(squares[x].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                self.play(FadeOut(squares_group_check, z))
                self.play(squares[x].animate.set_fill(GREEN, opacity=0.5))
                self.play(Write(Text("Found!", color = GREEN).next_to(squares[x], UP)))
                y = 0
                break
            else:
                z = Text("≠", color = WHITE, font_size = 40).next_to(squares_group, UP*0.8)
                self.play(Write(z))
                for j in range(3):
                    self.play(squares[x].animate.set_fill(RED, opacity=0.5), run_time = 0.35)
                    self.play(squares[x].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                self.play(FadeOut(squares_group_check, z))
                self.play(squares[x].animate.set_fill(RED, opacity=0.5))
                if l == r:
                    self.wait(0.5)
                    self.play(FadeOut(Group(squares[l], number_texts[l])))
                    break
                squares_group.next_to(squares[x], DOWN)
                if numbers[x] < target_number: 
                    # squares_group_check2 = squares[l:x+1]
                    squares_group_check2 = Group(squares[l:x+1], number_texts[l:x+1])
                    squares_group_check1 = Group(squares[x+1:r+1], number_texts[x+1:r+1])
                    squares_group_check3 = squares[x+1:r+1]
                    s = Tex(f"{target_number} greater {numbers[x]}", color = WHITE).next_to(squares[x], UP)
                    self.play(FadeOut(s), run_time = 2)
                    for j in range(3):
                        self.play(squares_group_check3.animate.set_fill(GREEN, opacity=0.35), run_time = 0.35)
                        self.play(squares_group_check3.animate.set_fill(YELLOW, opacity=0.35), run_time = 0.35)
                    self.play(squares_group_check3.animate.set_fill(BLACK, opacity=0))
                    # self.play(squares_group_check2.animate.set_fill(BLACK, opacity=1))
                    self.play(FadeOut(squares_group_check2))
                    self.play(squares_group_check1.animate.move_to(DOWN*2.5 + ORIGIN))
                    l = x + 1
                else:
                    # squares_group_check2 = squares[x:r+1]
                    squares_group_check2 = Group(squares[x:r+1], number_texts[x:r+1])
                    squares_group_check1 = Group(squares[l:x], number_texts[l:x])
                    squares_group_check3 = squares[l:x]
                    s = Tex(f"{target_number} less {numbers[x]}", color = WHITE).next_to(squares[x], UP)
                    self.play(FadeOut(s), run_time = 2)
                    for j in range(3):
                        self.play(squares_group_check3.animate.set_fill(GREEN, opacity=0.35), run_time = 0.35)
                        self.play(squares_group_check3.animate.set_fill(YELLOW, opacity=0.35), run_time = 0.35)
                    self.play(squares_group_check3.animate.set_fill(BLACK, opacity=0))
                    # self.play(squares_group_check2.animate.set_fill(BLACK, opacity=1))
                    self.play(FadeOut(squares_group_check2))
                    self.play(squares_group_check1.animate.move_to(DOWN*2.5 + ORIGIN))
                    r = x - 1
            self.play(FadeOut(a, b, fractions))

        if y == 1:
            self.play(Write(Text("Not Found!", color = RED).move_to(ORIGIN)))

        self.wait(2)  