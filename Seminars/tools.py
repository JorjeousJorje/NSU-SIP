import cv2 as cv
import numpy as np


def scale_img(image, scale: float):
    width, height = image.shape[1], image.shape[0]
    return cv.resize(image, (int(width * scale), int(height * scale)))


def clip_img(image, max_size: int):
    width, height = image.shape[1], image.shape[0]
    max_dim = max(width, height)
    ratio = float(max_size) / max_dim
    return cv.resize(image, (int(width*ratio), int(height*ratio)), interpolation=cv.INTER_CUBIC)


def add_noise(img, value):
    noise = np.random.normal(0, value, size=img.shape)
    img_rgb = np.clip(img + noise, 0, 255).astype(np.uint8)
    return img_rgb

def set_brightness(img, value):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    res = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return res

def set_contrast(img, value):
    lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)
    #-----Splitting the LAB image to different channels-----------------------—
    l, a, b = cv.split(lab)
    #-----Applying CLAHE to L-channel-----------------------------------------—
    clahe = cv.createCLAHE(clipLimit=value, tileGridSize=(8,8))
    cl = clahe.apply(l)
    #-----Merge the CLAHE enhanced L-channel with the a and b channel---------—
    limg = cv.merge((cl,a,b))
    #-----Converting image from LAB Color model to RGB model------------------—
    res = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return res