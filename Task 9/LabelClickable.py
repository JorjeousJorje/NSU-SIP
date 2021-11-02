from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent

class LabelClickable(QtWidgets.QLabel):


    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super(LabelClickable, self).__init__(parent)
        
        self.transform_points_from: list[tuple[int, int]] = []
        self.transform_points_to: list[tuple[int, int]] = []
    
       
    def mousePressEvent(self, event: QMouseEvent):
        
        if event.button() == Qt.MouseButton.LeftButton:
            if len(self.transform_points_from) == 4:
                self.transform_points_from.pop(0)
            
            x: int = event.pos().x()
            y: int = event.pos().y()
            
            if len(self.transform_points_from) < 4:
                pos: tuple[int, int] = (x, y)
                self.transform_points_from.append(pos)
                self.clicked.emit()
                
        elif event.button() == Qt.MouseButton.RightButton:
            if len(self.transform_points_to) == 4:
                self.transform_points_to.pop(0)
            
            x: int = event.pos().x()
            y: int = event.pos().y()
            
            if len(self.transform_points_to) < 4:
                pos: tuple[int, int] = (x, y)
                self.transform_points_to.append(pos)
                self.clicked.emit()