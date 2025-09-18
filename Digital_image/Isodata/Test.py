import cv2
import numpy as np
from manim import *

class ImageSegmentation(Scene):
    def construct(self):
        # Đọc ảnh
        image_path = "example.jpg"
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Kiểm tra nếu ảnh được đọc thành công
        if image is None:
            print("Error: Image not found or could not be read")
            return  # Dừng chương trình nếu ảnh không tồn tại

        # Hiển thị kích thước ảnh
        print("Image shape:", image.shape)
        
        # Áp dụng phân vùng Otsu
        ret, otsu_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Lưu ảnh phân vùng Otsu vào file
        cv2.imwrite("otsu_result.jpg", otsu_image)

        # Chuyển ảnh đầu vào và ảnh kết quả sang Mobject của Manim
        original_image = ImageMobject(image_path).scale(2)
        otsu_image_mobject = ImageMobject("otsu_result.jpg").scale(2)
        
        # Đưa ảnh gốc vào cảnh
        original_text = Text("Original Image", font="Segoe UI", font_size=22).set_color(WHITE)
        original_text.next_to(original_image, DOWN)

        self.play(FadeIn(original_image), Write(original_text))
        self.wait(1)

        # Chuyển sang ảnh sau khi phân vùng Otsu
        otsu_text = Text("Otsu Segmentation Result", font="Segoe UI", font_size=22).set_color(WHITE)
        otsu_text.next_to(otsu_image_mobject, DOWN)
        
        self.play(FadeOut(original_image), FadeOut(original_text))
        self.play(FadeIn(otsu_image_mobject), Write(otsu_text))

        # Giữ ảnh sau phân vùng trên màn hình
        self.wait(2)

