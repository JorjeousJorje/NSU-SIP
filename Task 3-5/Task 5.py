import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2


img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)


N = 15
image_list = []

for i in range(N):
    image_list.append(img + np.random.randint(-50, 50, size=img.shape))


result_image = np.array(sum(image_list) / N, dtype=np.uint8)
noised_image =  np.array(image_list[0], dtype=np.uint8)

noise_result_pair_image = np.hstack((img, result_image, noised_image))
print(noise_result_pair_image.shape)

win_name = 'Comparasion with N = ' + str(N)
height = noise_result_pair_image.shape[0]
lenght = noise_result_pair_image.shape[1]

cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_name, lenght, height) 
cv2.imshow(win_name, noise_result_pair_image)
cv2.waitKey(0)