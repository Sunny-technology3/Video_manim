from manim import *

def doc(a):
    with open(f"{a}", "r", encoding = "utf-8") as lf:
        lines = lf.readlines()   
    return lines

class CreatingTest(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        self.camera.background_opacity = 0.5

        lst = doc("Test.txt")
        title = Tex(lst[0], color = PINK,  font_size = 120).move_to(UP*2)
        self.play(Write(title))
        self.wait()

        rectangle = Rectangle(
            color = RED, height = 0.8, width = 10,  fill_opacity = 1
        )

        for i in range(len(lst)-1):   
            circle = Circle(
                radius = 0.4, color = RED, fill_opacity = 0.5
            )            
            self.play(Create(circle.move_to(DOWN*i)))
            self.play(Transform(circle, rectangle))
            rectangle.move_to(DOWN * (i+1))
            ttle = Text(lst[i+1]).move_to(DOWN * i)
            self.play(Write(ttle))
        self.wait()
