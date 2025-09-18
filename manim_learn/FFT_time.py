from manim import *

class DrawLine(Scene):
    def construct(self):
        A = Dot(ORIGIN, color = BLUE)  # Điểm A tại (0, 0, 0)
        B = Dot(2 * RIGHT + 1 * UP)  # Điểm B tại (2, 1, 0)

        line = Line(A.get_center(), B.get_center())

        self.play(DrawBorderThenFill(A), DrawBorderThenFill(B), Create(line))

        self.wait(2)