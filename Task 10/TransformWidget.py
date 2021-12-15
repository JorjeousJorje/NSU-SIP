from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
import cv2 as cv

from LabelClickable import LabelClickable

class TransformWidget(QtWidgets.QWidget):
    def __init__(self, name: str, main_window, transform) -> None:
        super(TransformWidget, self).__init__()
        uic.loadUi(r'ui/TransformWidget.ui', self)
        
        self.main_window = main_window
        self.transform = transform
        self.label: LabelClickable = self.main_window.transform_image_label
        
        self.setWindowTitle(name)
        
        
    @pyqtSlot()
    def refresh_points(self) -> None:
        self.label.transform_points_from.clear()
        self.label.transform_points_to.clear()
        self.main_window.update_transforms_label(self.main_window.image_transformed)
        
    @pyqtSlot()
    def reset_transform(self) -> None:
        self.main_window.image_transformed = self.main_window.image
        self.main_window.update_transforms_label(self.main_window.image)
        
        
    @pyqtSlot()
    
    def transform_image(self) -> None:
        result_shape = None
        
        if self.main_window.image_transformed is not None:
            if self.default_shape.isChecked():
                result_shape: tuple[int, int] = self.main_window.image_transformed.shape[0: 2]
            else:
                width: int = self.width_spin.value()
                height: int = self.height_spin.value()
                result_shape: tuple[int, int] = (width, height)
            
            transformed: np.ndarray = self.transform.transform(self.main_window.image_transformed,
                                                                self.label.transform_points_from,
                                                                self.label.transform_points_to,
                                                                result_shape)

            if transformed is not None:
                self.main_window.image_transformed = transformed
                self.main_window.update_transforms_label(transformed)