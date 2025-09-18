import cv2
import numpy as np
from matplotlib import pyplot as plt

# Đọc ảnh gốc ở chế độ grayscale
image = cv2.imread('example.jpg', 0)

# Đảo ngược ảnh để vùng đen thành trắng và vùng trắng thành đen
inverted_image = cv2.bitwise_not(image)

# Tạo kernel (hạt nhân) cho phép toán dilation
kernel = np.ones((5,5), np.uint8)

# Thực hiện phép toán dilation trên ảnh đã đảo ngược
dilated_image = cv2.dilate(inverted_image, kernel, iterations=1)

# Đảo ngược lại ảnh đã dilated để quay về vùng đen ban đầu
result = cv2.bitwise_not(dilated_image)

# Hiển thị ảnh
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(image, cmap='gray')

plt.subplot(1, 3, 2)
plt.title("Inverted Image")
plt.imshow(inverted_image, cmap='gray')

plt.subplot(1, 3, 3)
plt.title("Dilated Black Regions")
plt.imshow(result, cmap='gray')

plt.show()
