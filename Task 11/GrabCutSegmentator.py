import enum
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtGui import QKeyEvent
import cv2 as cv
import numpy as np
from itertools import cycle

class GrubCutMode(enum.IntEnum):
    MaskMode = cv.GC_INIT_WITH_MASK
    RectMode = cv.GC_INIT_WITH_RECT

class GrabCutSegmentator(QObject):
    
    
    def __init__(self, mask_shape: tuple[int, int]) -> None:
        self.rect: tuple[int, int, int, int] = None
        self.init_mask_value: int = 100
        self.mask: np.ndarray = np.full(mask_shape, self.init_mask_value, dtype=np.uint8)
        self.modes: list[GrubCutMode] = [GrubCutMode.RectMode, GrubCutMode.MaskMode]
        self.mode_iter: cycle = cycle(self.modes)
        self.current_mode: GrubCutMode = GrubCutMode.RectMode
        self.bgd: np.ndarray = np.zeros((1, 65), dtype=np.float64)
        self.fgd: np.ndarray = np.zeros((1, 65), dtype=np.float64)
        
    
    def eventFilter(self, obj: QObject, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Tab:
            self.change_mode()
            obj.emit_mode_state.emit(str(self.current_mode))
        elif event.key() == Qt.Key.Key_Return:
            segmented = self.perform_grabcut(obj.image.copy())
            if segmented is not None:
                obj.current_image = segmented
                obj.update_image_label(obj.current_image)
        
    def insert_rect_inside_mask(self) -> None:
        x_left = self.rect[0]
        x_right = self.rect[2]
        y_left = self.rect[1]
        y_right = self.rect[3]
        
        self.mask[y_left: y_right, x_left: x_right] = np.where((self.mask[y_left : y_right, x_left: x_right] == cv.GC_BGD) | 
                                                                (self.mask[y_left : y_right, x_left: x_right] == cv.GC_FGD), 
                                                                self.mask[y_left : y_right, x_left: x_right],  
                                                                cv.GC_PR_FGD)
    def change_mode(self) -> None:
        self.current_mode = next(self.mode_iter)
        
    def clear_mask(self) -> None:
        self.rect = None
        self.mask[:] = self.init_mask_value
        
    def set_rect(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> None:
        self.rect = start_pos + end_pos if start_pos < end_pos else end_pos + start_pos

    def rect_grabcut(self, image: np.ndarray) -> np.ndarray:
        mask, _, _ = cv.grabCut(image, None, 
                                self.rect, self.bgd, 
                                self.fgd, iterCount=1, 
                                mode=self.current_mode)
        return mask
    
    def mask_grabcut(self, image: np.ndarray) -> np.ndarray:
        mask, _, _ = cv.grabCut(image, self.mask, 
                                None, self.bgd, 
                                self.fgd, iterCount=1, 
                                mode=self.current_mode)
        return mask
    
    def apply_mask(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        output_mask: np.ndarray = np.where((mask == cv.GC_BGD) | (mask == cv.GC_PR_BGD), 0, 255)
        output_mask = output_mask.astype(np.uint8)
        segmented = np.bitwise_and(image, output_mask[..., None])
        return segmented
    
    def perform_grabcut(self, image: np.ndarray) -> np.ndarray:
        mask: np.ndarray = None
        if self.current_mode == GrubCutMode.RectMode:
            
            if self.rect is not None:
                mask = self.rect_grabcut(image)
                
        elif not np.all(self.mask == self.init_mask_value):
            if self.rect is not None:
                self.insert_rect_inside_mask()
            
            self.mask[self.mask == self.init_mask_value] = cv.GC_BGD
            mask = self.mask_grabcut(image)
        
        if mask is not None:
            return self.apply_mask(image, mask)
        return None