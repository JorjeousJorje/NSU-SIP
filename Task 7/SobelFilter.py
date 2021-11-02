from FilterType import FilterType, np
import cv2 as cv
from abc import abstractmethod

class SobelFilter(FilterType):
    
    def __init__(self, img: np.ndarray) -> None:
        super().__init__(img)
        self.depths: list = [-1, cv.CV_32F, cv.CV_64F]
        self.current_depth: int = self.depths[0]
        
        self.dx: int = 1
        self.dy: int = 1
        self.current_delta: float = 0.0
        
        
    def filter_image(self, img: np.ndarray) -> np.ndarray:
        img_sobel = cv.Sobel(src=img, 
                            ddepth=self.current_depth, 
                            dx=self.dx, 
                            dy=self.dy, 
                            ksize=2 * self.ksize + 1,
                            delta=self.current_delta)
        return img_sobel
    
    def update_ksize(self, ksize: int) -> np.ndarray:
        if ksize >= self.dx and ksize >= self.dy:
            self.ksize = ksize
        return self.filter_image(self.noised_img)
    
    def update_delta(self, value: int) -> np.ndarray:
        self.current_delta = value / 100
        return self.filter_image(self.noised_img)
         
    def update_depth(self, value: int) -> np.ndarray:
        self.current_depth = self.depths[value]
        return self.filter_image(self.noised_img)
        
    def update_dx(self, value: int) -> np.ndarray:
        if (self.ksize >= value) and (self.dy + value >= 0):
            self.dx = value
        return self.filter_image(self.noised_img)
        
    def update_dy(self, value: int) -> np.ndarray:
        if (self.ksize >= value) and (self.dx + value >= 0):
            self.dy = value
        return self.filter_image(self.noised_img)
    

    def reset_params(self) -> None:
        self.current_depth: int = self.depths[0]
        
        self.dx: int = 1
        self.dy: int = 1
        self.current_delta: float = 0.0
        self.ksize = 0