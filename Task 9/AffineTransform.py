import cv2 as cv
import numpy as np


class AffineTransform:
    
    
    
    def __init__(self) -> None:
        pass
    
    
    @staticmethod
    def transform(img: np.ndarray, 
                  points_from: list[tuple[int, int]], 
                  points_to: list[tuple[int, int]], 
                  img_shape: tuple[int, int]) -> np.ndarray:
        
        if len(points_from) < 3 or len(points_to) < 3:
            print("<AffineTransform>: not enough points!")
            return None
        
        

        pts1 = np.float32(points_from[0: 3])
        pts2 = np.float32(points_to[0: 3])

        M = cv.getAffineTransform(pts1, pts2)
        dst = cv.warpAffine(img, M, img_shape)
        return dst