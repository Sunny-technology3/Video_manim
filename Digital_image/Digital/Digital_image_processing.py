from manim import *
import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt

class DigitalImage(Scene):
    def logo(self):
        image = ImageMobject(r"C:\Users\ADMIN\OneDrive\Tài liệu\Python\VSC\ptit-logo-circle.jpg")       
        '# Init logo start at mid of scene'
        image_cp = image.copy().scale(3)  
        image.scale(0.5).to_edge(UP).to_edge(LEFT).shift(LEFT * 0.4, UP * 0.4) 
        self.play(Succession( FadeIn(image_cp), Transform(image_cp, image)))        
        txt_intro = Text('''STDR2024 @EIC&DSP LAB\nDesigned by Le Minh Nam''',
                        font= "Segoe UI", font_size= 20
                        ).scale(2).move_to(ORIGIN)
        txt_intro.set_color(BLACK)
        self.play(Write(txt_intro), run_time = 1.5)
        self.play(txt_intro.animate.scale(0.3).to_edge(DR).shift(DOWN * 0.35, RIGHT * 0.35))
        txt_header = Text("Digital Image Processing", color = BLACK, font= "JetBrains Mono", font_size= 38).move_to(ORIGIN)
        self.play(Succession(Write(txt_header), ApplyWave(txt_header, scale_factor = 1.2), txt_header.animate.to_edge(UP).scale(0.8)))

    def construct(self):
        self.camera.background_color = WHITE
        self.logo()

        img = cv2.imread("example.jpg")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("processed_example.jpg", img)

        original_image = ImageMobject("processed_example.jpg").scale(0.6)
        self.play(Succession(FadeIn(original_image), original_image.animate.shift(LEFT * 5)))
        self.wait(1)

        red_overlay = Rectangle(width=3 * 0.1, height=3 * 0.1, color=RED, fill_opacity=0)
        overlay_x = 17 * 0.1  
        overlay_y = 16 * 0.1 
        red_overlay.move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))
        self.play(Create(red_overlay))

        cropped_img = img[250:400, 350:500]    
        cropped_img = cv2.resize(cropped_img, (600, 600), interpolation=cv2.INTER_LANCZOS4)    
        cv2.imwrite("cropped_image.jpg", cropped_img)  
        cropped_image_mobject = ImageMobject("cropped_image.jpg").scale(0.22).move_to(original_image.get_corner(UL) + np.array([overlay_x, -overlay_y, 0]))  
        self.play(FadeIn(cropped_image_mobject), cropped_image_mobject.animate.scale(3.5).next_to(original_image, RIGHT*6))

        red_overlay1 = Rectangle(width=3 * 0.1, height=3 * 0.1, color=RED, fill_opacity=0)
        overlay_x1 = 15 * 0.1  
        overlay_y1 = 12 * 0.1  
        red_overlay1.move_to(cropped_image_mobject.get_corner(UL) + np.array([overlay_x1, -overlay_y1, 0]))
        self.play(Create(red_overlay1))
        
        #tạo ma trận số
        cropped_img1 = cropped_img[50:56, 50:56]
        cv2.imwrite("cropped1_image.jpg", cropped_img1)
        cropped_image_mobject1 = ImageMobject("cropped1_image.jpg").scale(0.22).move_to(cropped_image_mobject.get_corner(UL) + np.array([overlay_x1, -overlay_y1, 0]))  
        self.play(FadeIn(cropped_image_mobject1), cropped_image_mobject1.animate.scale(300).next_to(cropped_image_mobject, RIGHT*6.5))
        self.wait(1)
        matrix = np.array(cropped_img1)
        grid = VGroup()
        number_of_cols = len(matrix[0])
        number_of_rows = len(matrix)
        square_size = 0.5  
        for i in range(number_of_rows):
            for j in range(number_of_cols):
                square = Square(side_length=square_size).set_stroke(BLACK, 1)
                square.move_to((j * square_size, -i * square_size, 0))
                number = Text(str(matrix[i][j]), color=BLACK, font="SF Pro", font_size=18).move_to(square.get_center())
                grid.add(VGroup(square, number))
        grid.move_to(cropped_image_mobject1.get_center())
        self.play(FadeOut(cropped_image_mobject1), FadeIn(grid))
        
        self.play(FadeOut(red_overlay, red_overlay1, cropped_image_mobject, original_image))
        self.play(grid.animate.move_to(LEFT*4))

        img = Image.open('cropped1_image.jpg')  
        data = np.array(img)       
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for i in range(300, 306):
            for j in range(400, 406):
                x = np.append(x, i)
                y = np.append(y, j)
                z = np.append(z, data[i-300][j-400])
        # Tạo figure và axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Vẽ đồ thị 3D
        colors = [
            (0.0, 0.5, 0.0),  # Xanh đậm
            (0.0, 1.0, 0.0),  # Xanh nhạt
            (0.0, 0.0, 0.0)  # Đen
        ]
        for i in range(len(x)):
            ax.plot([x[i], x[i]], [y[i], y[i]], [0, z[i]], color=colors[i % len(colors)], linestyle='-')
        ax.set_xlim(280, 330)
        ax.set_ylim(380, 430)
        ax.set_zlim(0, 250)
        plt.savefig('temp_plot.jpg', bbox_inches='tight', dpi=300)
        image = ImageMobject('temp_plot.jpg').scale(0.6).next_to(grid, RIGHT*6)
        self.play(FadeIn(image))
        self.wait(0.5)

        self.play(FadeOut(grid, image), FadeIn(cropped_image_mobject.move_to(grid.get_center())))
       
        img = Image.open('cropped_image.jpg')  
        data = np.array(img)       
        x = np.array([])
        y = np.array([])
        z = np.array([])
        for i in range(250, 400):
            for j in range(350, 500):
                x = np.append(x, i)
                y = np.append(y, j)
                z = np.append(z, data[i-250][j-350])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colors = [
            (0.0, 0.5, 0.0),  
            (0.0, 1.0, 0.0),  
            (0.0, 0.0, 0.0) 
        ]
        for i in range(len(x)):
            ax.plot([x[i], x[i]], [y[i], y[i]], [0, z[i]], color=colors[i % len(colors)], linestyle='-')
        ax.set_xlim(200, 420)
        ax.set_ylim(300, 520)
        ax.set_zlim(0, 250)
        plt.savefig('temp_plot1.jpg', bbox_inches='tight', dpi=300)
        image1 = ImageMobject('temp_plot1.jpg').scale(0.6)
        # .next_to(cropped_image_mobject, RIGHT*6)
        self.play(FadeIn(image1), image1.animate.move_to(RIGHT*2.5))
        self.wait(1)
        self.play(FadeOut(cropped_image_mobject), FadeIn(original_image.move_to(cropped_image_mobject.get_center())))
        image2 = ImageMobject("digital.jpg").scale(2)
        self.play(FadeOut(image1), FadeIn(image2.move_to(image1.get_center())))

        self.wait(5)