from manim import *
import cv2
import numpy
from PIL import Image
import operator
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import io

class ShowImage(Scene):
    def logo(self):
        img = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg").move_to(ORIGIN)
        self.play(Succession(FadeIn(img, run_time=1), img.animate.scale(0.5).to_corner(UP+LEFT).shift(LEFT*0.3 + UP * 0.3)))      
        a1 = Text("STDR2024 @EIC&DSP LAB\nDesigned by Le Minh Nam", font= "Segoe UI", color = BLACK, font_size=30).move_to(ORIGIN)
        self.play(Succession(Write(a1), a1.animate.to_corner(DOWN+RIGHT).shift(RIGHT*1.3 + DOWN*0.5).scale(0.6)))
        a2 = Text("Digital Image Processing", font= "Segoe UI", color = BLACK, font_size=40).move_to(ORIGIN)
        self.play(Succession(Write(a2), ApplyWave(a2, scale_factor = 1.2),a2.animate.to_edge(UP).scale(0.8)))

    def construct(self):
        self.camera.background_color = WHITE
        self.logo()

        img = cv2.imread("example.jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("processed_example.jpg", img)
        