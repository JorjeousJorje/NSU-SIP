import cv2 as cv
import numpy as np

class HoughCirclesDetector:
    
    
    def __init__(self, img: np.ndarray) -> None:
        self.image: np.ndarray = img
        
        self.dp: int = 1
        
        self.min_dist: float = 20.0
        self.min_dist_scale: float = 1.0
        
        self.param1: float = 50.0
        self.param1_scale: float = 1.0
        
        self.param2: float = 30.0
        self.param2_scale: float = 1.0
        
        self.min_rad: int = 1
        self.max_rad: int = 6

    def detect_circles(self) -> np.ndarray:
        circles = cv.HoughCircles(image=self.image,
                                  method=cv.HOUGH_GRADIENT,
                                  dp=self.dp,
                                  minDist=self.min_dist,
                                  param1=self.param1,
                                  param2=self.param2,
                                  minRadius=self.min_rad,
                                  maxRadius=self.max_rad)
        
        return circles
     


    def update_dp(self, dp: int) -> np.ndarray:
         self.dp = dp
         return self.detect_circles()
     
    def update_min_dist(self, min_dist: float) -> np.ndarray:
         self.min_dist = min_dist / self.min_dist_scale
         return self.detect_circles()
     
    def update_param1(self, param1: float) -> np.ndarray:
         self.param1 = param1 / self.param1_scale
         return self.detect_circles()
     
    def update_param2(self, param2: float) -> np.ndarray:
         self.param2 = param2 / self.param2_scale
         return self.detect_circles()
     
    def update_min_rad(self, min_rad: int) -> np.ndarray:
         if self.max_rad > min_rad:
              self.min_rad = min_rad
         return self.detect_circles()
     
    def update_max_rad(self, max_rad: int) -> np.ndarray:
         if self.min_rad < max_rad:
               self.max_rad = max_rad
         return self.detect_circles()
     
        