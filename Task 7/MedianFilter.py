from FilterType import FilterType, np
import cv2 as cv

class MedianFilter(FilterType):
    def __init__(self, img: np.ndarray) -> None:
        super().__init__(img)
        
        
    def filter_image(self, img: np.ndarray) -> np.ndarray:
        
        img_filtered = cv.medianBlur(img, ksize=2 * self.ksize + 1)
        return img_filtered

    def reset_params(self) -> None:
        self.ksize = 0