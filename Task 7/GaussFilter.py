from FilterType import FilterType, np
import cv2 as cv

class GaussFilter(FilterType):
    
    def __init__(self, img: np.ndarray) -> None:
        super().__init__(img)
        self.sigmaX: float = 0.0
        self.sigmaY: float = 0.0
         
    def filter_image(self, img: np.ndarray) -> np.ndarray:
        
        img_blur = cv.GaussianBlur(img, 
                                   ksize=(2 * self.ksize + 1, 2 * self.ksize + 1), 
                                   sigmaX=self.sigmaX, 
                                   sigmaY=self.sigmaY)
        return img_blur

    def update_sigma_x(self, value: int) -> np.ndarray:
        self.sigmaX = float(value)
        return self.filter_image(self.noised_img)
        
    def update_sigma_y(self, value: int) -> np.ndarray:
        self.sigmaY = float(value)
        return self.filter_image(self.noised_img)
    
    def reset_params(self) -> None:
        self.ksize = 0
        self.sigmaX = 0.0
        self.sigmaY = 0.0

    