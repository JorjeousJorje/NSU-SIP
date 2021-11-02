import re
import enum
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from itertools import cycle

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent


from GrabCutSegmentator import GrabCutSegmentator
from Drawer import SegmentatorDrawer
from LabelClickable import LabelClickable

class MainWindow(QtWidgets.QMainWindow):
    
    emit_mode_state = pyqtSignal(str)
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi(r'ui/MainWindow.ui', self)
        
        self.image: np.ndarray = None
        self.current_image: np.ndarray = None
        self.drawer: SegmentatorDrawer = None
        self.segmentator: GrabCutSegmentator = None
    
    def reset_window(self):
        if self.image is not None:
            self.current_image = self.image.copy()
            self.segmentator.clear_mask()
            self.update_image_label(self.current_image)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:

        if event.key() == Qt.Key.Key_Space:
            self.reset_window()
            
        if self.segmentator is not None:
            self.segmentator.eventFilter(self, event)
        
        if self.drawer is not None:
            self.drawer.eventFilter(None, event)
            
    @staticmethod
    def get_qimage(image: np.ndarray) -> QPixmap:
        qimage = QImage(image, image.shape[1], 
                        image.shape[0], image.strides[0], 
                        QImage.Format_RGB888)
        
        qimage = qimage.rgbSwapped()
        return QPixmap.fromImage(qimage)
    
    def update_image_label(self, image: np.ndarray) -> None:
        qimage = MainWindow.get_qimage(image)
        self.image_label.setPixmap(qimage)
        
    def resize_to_label(self, image: np.ndarray):
        label_size: QSize = self.image_label.size()
        dim: tuple[int, int] = (label_size.width(), label_size.height())
        self.image: np.ndarray = cv.resize(src=image, dsize=dim, interpolation=cv.INTER_AREA)
        
    @pyqtSlot()
    def load_image(self) -> None:
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        
        self.image: np.ndarray = cv.imread(path)
        
        def has_cyrillic(text: str):
            return bool(re.search('[а-яА-Я]', text))
        
        if has_cyrillic(path):
            print("Path contains cyrillic characters, opencv don't like it!")
            return
        if self.image is None:
            print("Can't read image. Check choosen file!")
            return
        
        self.init_attributes()
        
    def init_attributes(self) -> None:
        self.resize_to_label(self.image)
        self.current_image = self.image.copy()
        self.segmentator = GrabCutSegmentator(mask_shape=self.image.shape[0: 2])
        self.drawer = SegmentatorDrawer(self)
        
        self.image_label.mouse_moved.connect(self.drawer.draw_on_move)
        
        self.update_image_label(self.image)
        self.emit_mode_state.emit(str(self.segmentator.current_mode))
        
    