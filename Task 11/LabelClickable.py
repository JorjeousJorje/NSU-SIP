from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QKeyEvent

import cv2 as cv
import enum


class LabelClickable(QtWidgets.QLabel):
        
    mouse_moved = pyqtSignal(QtWidgets.QLabel)
    
    def __init__(self, parent=None):
        super(LabelClickable, self).__init__(parent)
        
        self.mouse_left_clicked: bool = False
        self.left_top_pos: tuple[int, int] = tuple()
        self.current_mouse_pos: tuple[int, int] = tuple()
        
    
    def get_pos_tuple(self, event: QMouseEvent) -> tuple[int, int]:
        x: int = event.pos().x()
        y: int = event.pos().y()
        return (x, y)
    
    def mousePressEvent(self, event: QMouseEvent):
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_left_clicked = True
            self.left_top_pos = self.get_pos_tuple(event)
            self.current_mouse_pos = self.get_pos_tuple(event)
            self.mouse_moved.emit(self)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_left_clicked = False
            self.current_mouse_pos = self.get_pos_tuple(event)
            self.mouse_moved.emit(self)
        
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.mouse_left_clicked:
            self.current_mouse_pos = self.get_pos_tuple(event)
            self.mouse_moved.emit(self)