import cv2 as cv
import numpy as np



class HarrisDetector:
    def __init__(self) -> None:
        
        self.blocksize: int = 1
        self.ksize: int = 1
        self.k: float = 100.0
        
        
    def get_response(self, color_image: np.ndarray) -> np.ndarray:
        gray: np.ndarray = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
        
        corners = cv.cornerHarris(src=gray, 
                                  blockSize=self.blocksize,
                                  ksize=self.ksize,
                                  k=self.k)
        return corners
    