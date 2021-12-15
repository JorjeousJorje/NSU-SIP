import cv2 as cv


def scale_img(image, scale: float):
    width, height = image.shape[1], image.shape[0]
    return cv.resize(image, (int(width * scale), int(height * scale)))


def clip_img(image, max_size: int):
    width, height = image.shape[1], image.shape[0]
    max_dim = max(width, height)
    ratio = float(max_size) / max_dim
    return cv.resize(image, (int(width*ratio), int(height*ratio)), interpolation=cv.INTER_CUBIC)