import cv2 as cv
import numpy as np


class PerspectiveTransform:
    
    
    
    def __init__(self) -> None:
        pass
    
    
    @staticmethod
    def transform(img: np.ndarray, 
                  points_from: list[tuple[int, int]], 
                  points_to: list[tuple[int, int]], 
                  img_shape: tuple[int, int]) -> np.ndarray:
        
        if not points_from:
            points_from = [(0, 0), (0, img_shape[0]), (img_shape[0], img_shape[1]), (img_shape[1], 0)]
        
        if len(points_from) != 4 or len(points_to) != 4:
            print("<PerspectiveTransform>: not enough points!")
            return None
        
        pts1 = np.float32(points_to)
        pts2 = np.float32(points_from)
        
        
        M = cv.getPerspectiveTransform(pts1, pts2)
        dst = cv.warpPerspective(img, M, img_shape)
        return dst