from manim import *
import cv2

def doc(a):
    with open(f"{a}", "r", encoding = "utf-8") as lf:
        lines = lf.read().split()   
    return lines

class LinearSearch(Scene):
    def logo(self):
        img = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg").move_to(ORIGIN)
        self.play(Succession(FadeIn(img, run_time=1), img.animate.scale(0.5).to_corner(UP+LEFT).shift(LEFT*0.3 + UP * 0.3)))      
        a1 = Text("STDR2024 @EIC&DSP LAB\nDesigned by Le Minh Nam", font= "Segoe UI", color = WHITE, font_size=30).move_to(ORIGIN)
        self.play(Succession(Write(a1), a1.animate.to_corner(DOWN+RIGHT).shift(RIGHT*1.3 + DOWN*0.5).scale(0.6)))

    def construct(self):
        self.camera.background_color = BLACK
        self.logo()

        a2 = Text("LinearSearch", font= "Segoe UI", color = WHITE, font_size=50).move_to(ORIGIN)
        self.play(Succession(Write(a2), Indicate(a2, scale_factor = 1.2),a2.animate.to_edge(UP).scale(0.7)))

        numbers = doc("linearsearch.txt")
        x = 1

        target_number = numbers[len(numbers) - 1]
        target_index = numbers.index(target_number)
        target_text = Text(f"Find: {target_number}", font="Comic Sans MS", color = WHITE, font_size=40).next_to(a2, DOWN)
        self.play(Write(target_text))

        squares = VGroup(*[Square(side_length=1, color=WHITE).shift(RIGHT * i) for i in range(len(numbers) - 1)])
        self.add(squares)

        number_texts = VGroup(*[Text(str(num), color = WHITE).move_to(square.get_center()) for num, square in zip(numbers, squares)])
        self.add(number_texts)

        squares_group = Group(squares, number_texts)           
        squares_group.next_to(target_text, DOWN*1.5, target_text.height * 5)

        squares_check = Square(side_length=1, color = WHITE)
        target_number_check = Text(str(target_number), color = WHITE).move_to(squares_check.get_center())
        squares_group_check = Group(squares_check, target_number_check).next_to(squares[0], UP*8.5)

        self.play(FadeIn(squares_group_check))

        for i in range(len(numbers)-1): 
            squares_group = Group(squares[i], number_texts[i])
            self.play(squares[i].animate.set_fill(YELLOW, opacity=0.5))
            squares_group.next_to(squares[i], UP)
            self.wait(1)

            if numbers[i] == target_number:
                a = Text("=", color = WHITE, font_size = 40).next_to(squares_group, UP*1.45)
                self.add(a)
                for j in range(3):
                    self.play(squares[i].animate.set_fill(GREEN, opacity=0.5), run_time = 0.35)
                    self.play(squares[i].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                self.play(squares[i].animate.set_fill(GREEN, opacity=0.5))
                self.play(FadeOut(squares_group_check, a))
                self.play(Write(Text("Found!", color = GREEN).next_to(squares[i], UP)))
                x  = 0
                break

            else:
                a = Text("≠", color = WHITE, font_size = 40).next_to(squares_group, UP*1.45)
                self.add(a)
                for j in range(3):
                    self.play(squares[i].animate.set_fill(RED, opacity=0.5), run_time = 0.35)
                    self.play(squares[i].animate.set_fill(YELLOW, opacity=0.5), run_time = 0.35)
                self.play(squares[i].animate.set_fill(RED, opacity=0.5))
                squares_group.next_to(squares[i], DOWN)
                self.play(FadeOut(a))
                if i!= len(numbers) -2:
                    self.play(squares_group_check.animate.shift(RIGHT))
                else:
                    self.play(FadeOut(squares_group_check))

        if x == 1:
            self.play(Write(Text("Not Found!", color = RED).next_to(squares, UP*9)))

        self.wait(2)  
