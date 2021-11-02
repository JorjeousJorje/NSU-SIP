import enum

from itertools import cycle
from typing import Callable
from PyQt5.QtCore import QObject, Qt, pyqtSlot, QEvent
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent

import cv2 as cv
import numpy as np
from LabelClickable import LabelClickable

class DrawButton(enum.IntEnum):
    DFore = Qt.Key.Key_Q
    DBack = Qt.Key.Key_W
    Rect = Qt.Key.Key_T

class SegmentatorDrawerMode(enum.IntEnum):
    DrawMask = 0
    DrawRect = 1

class Drawer:
    def __init__(self) -> None:
        pass
    
    def draw_circle(self, image: np.ndarray, center: tuple[int, int], color, thickness: int) -> np.ndarray:
        return cv.circle(image, center, thickness, color, -1)
    
    def draw_rect(self, image: np.ndarray, rect: tuple[int, int, int, int], color, thickness: int) -> np.ndarray:
        start_pos: tuple[int, int] = rect[0], rect[1]
        end_pos: tuple[int, int] = rect[2], rect[3]
        return cv.rectangle(image, start_pos, end_pos, color, thickness)
    
    
class SegmentatorDrawer(Drawer, QObject):
    
    def __init__(self, main_window) -> None:
        QObject.__init__(self)
        Drawer.__init__(self)
        
        self.mask_color: int = cv.GC_BGD
        self.main_window = main_window
        self.segmentator = self.main_window.segmentator
        self.mode: SegmentatorDrawerMode = SegmentatorDrawerMode.DrawRect
        
        self.colors = {DrawButton.DFore: (255, 255, 255),
                       DrawButton.DBack: (0, 0, 0),
                       DrawButton.Rect:  (0, 255, 0)}
    
        self.current_color = self.colors[DrawButton.Rect]
    
    def eventFilter(self, obj: QObject, event: QKeyEvent) -> None:
            
        if event.key() == DrawButton.DFore:
            self.mode = SegmentatorDrawerMode.DrawMask
            self.mask_color = cv.GC_FGD
            self.set_color(DrawButton.DFore)
            
        elif event.key() == DrawButton.DBack:
            self.mode = SegmentatorDrawerMode.DrawMask
            self.mask_color = cv.GC_BGD
            self.set_color(DrawButton.DBack)
            
        elif event.key() == DrawButton.Rect:
            self.mode = SegmentatorDrawerMode.DrawRect
            self.set_color(DrawButton.Rect)
            
    def set_color(self, button: DrawButton) -> None:
        self.current_color = self.colors[button]
        
    @pyqtSlot(LabelClickable)
    def draw_on_move(self, label: LabelClickable) -> None:
        
        if self.mode == SegmentatorDrawerMode.DrawRect:
            self.segmentator.set_rect(label.left_top_pos, label.current_mouse_pos)
            with_rect = self.draw_rect(self.main_window.current_image.copy(), self.segmentator.rect, self.current_color, 2)
            self.main_window.update_image_label(with_rect)
        
        if self.mode == SegmentatorDrawerMode.DrawMask:
            self.draw_circle(self.main_window.current_image, label.current_mouse_pos, self.current_color, 8)
            self.segmentator.mask = self.draw_circle(self.segmentator.mask, label.current_mouse_pos, self.mask_color, 8)
            
            if self.segmentator.rect is not None:
                with_rect = self.draw_rect(self.main_window.current_image.copy(), self.segmentator.rect, (0, 255, 0), 2)
                self.main_window.update_image_label(with_rect)
                return
            self.main_window.update_image_label(self.main_window.current_image) 