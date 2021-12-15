import cv2 as cv
import numpy as np



class TomachiDetector:
    def __init__(self) -> None:
        
        self.max_corners: int = 1
        self.quality_level: float = 0.01
        self.min_distance: float = 1.0
        self.blocksize: int = 3
        
        
    def get_response(self, color_image: np.ndarray) -> np.ndarray:
        gray: np.ndarray = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
        
        corners = cv.goodFeaturesToTrack(image=gray, 
                                         maxCorners=self.max_corners,
                                         qualityLevel=self.quality_level,
                                         minDistance=self.min_distance,
                                         blockSize=self.blocksize)
        
        return corners
    