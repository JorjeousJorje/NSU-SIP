import re
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QSize, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2 as cv

from LabelClickable import LabelClickable
from HarrisDetectorWidget import HarrisDetectorWidget
from TomachiDetectorWidget import TomachiDetectorWidget
from TransformWidget import TransformWidget

from AffineTransform import AffineTransform
from PerspectiveTransform import PerspectiveTransform

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi(r'ui/MainWindow.ui', self)
        
        self.image: np.ndarray = None
        self.image_transformed: np.ndarray = None
        
        self.detector_widgets: dict[str, QtWidgets.QWidget] = {'Tomachi': TomachiDetectorWidget(main_window=self)}
        
        self.transform_widgets: dict[str, QtWidgets.QWidget] = {'Perspective': TransformWidget('Perspective', self, PerspectiveTransform()),
                                                                 'Affine': TransformWidget('Affine', self, AffineTransform())}
        
        self.current_detector_widget: QtWidgets.QWidget = None
        
        self.transform_image_label.clicked.connect(self.draw_circle_on_click)
        
    @staticmethod
    def get_qimage(image) -> QImage:
        qimage = QImage(image, 
                        image.shape[1], 
                        image.shape[0], 
                        image.strides[0], 
                        QImage.Format_RGB888)
        
        qimage = qimage.rgbSwapped()
        return QPixmap.fromImage(qimage)
    
    @pyqtSlot()
    def draw_circle_on_click(self):
        if self.image_transformed is not None:
            copy = self.image_transformed.copy()
            
            for pos in self.transform_image_label.transform_points_from:
                cv.circle(copy, pos, 5, (0, 0, 255), -1)
            for pos in self.transform_image_label.transform_points_to:
                cv.circle(copy, pos, 5, (0, 255, 0), -1)
            self.update_transforms_label(copy)
        
    def update_no_transforms_label(self, image: np.ndarray) -> None:
        qimage = MainWindow.get_qimage(image)
        self.no_transform_image_label.setPixmap(qimage)
        
    def update_transforms_label(self, image: np.ndarray) -> None:
        qimage = MainWindow.get_qimage(image)
        self.transform_image_label.setPixmap(qimage)
        
    def __resize_to_label(self, image: np.ndarray):
        label_size: QSize = self.transform_image_label.size()
        dim: tuple[int, int] = (label_size.width(), label_size.height())
        self.image = cv.resize(src=image, dsize=dim, interpolation=cv.INTER_AREA)
        
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
        
        self.__resize_to_label(self.image)
        self.image_transformed = self.image
        self.update_no_transforms_label(self.image)
        self.update_transforms_label(self.image_transformed)
      
      
    def close_current_widget(self) -> None:
        if self.current_detector_widget is not None:
            
            if self.image is not None:
                self.update_no_transforms_label(self.image)
                self.update_transforms_label(self.image_transformed)
                
            self.current_detector_widget.close()
        
    @pyqtSlot()
    def show_tomachi_widget(self) -> None:
        self.close_current_widget()
        self.current_widget = self.detector_widgets["Tomachi"]
        self.current_widget.show()
        
    @pyqtSlot()
    def show_affine_widget(self) -> None:
        self.transform_widgets["Perspective"].close()
        current_widget = self.transform_widgets["Affine"]
        current_widget.show()
        
    @pyqtSlot()
    def show_perspective_widget(self) -> None:
        self.transform_widgets["Affine"].close()
        current_widget = self.transform_widgets["Perspective"]
        current_widget.show()
        
        
    