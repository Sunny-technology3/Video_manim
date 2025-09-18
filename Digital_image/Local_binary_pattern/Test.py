from manim import *
import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt

class ShowImage(Scene):
    
    def construct(self):

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

        self.play(FadeIn(axes))

        stems = VGroup()
        lbph_number = VGroup()
        histogram_dict = np.array([3, 3, 2, 1, 3, 1])
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