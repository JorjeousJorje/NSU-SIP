from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
import cv2 as cv

from TomachiDetector import TomachiDetector


class TomachiDetectorWidget(QtWidgets.QWidget):
    def __init__(self, main_window) -> None:
        super(TomachiDetectorWidget, self).__init__()
        uic.loadUi(r'ui/TomachiWidget.ui', self)
        
        self.detector: TomachiDetector = TomachiDetector()
        
        self.transform_response: np.ndarray = None
        self.response: np.ndarray = None
        
        self.main_window = main_window
    
    
    def __set_features(self) -> None:
        
        corners: np.ndarray = np.int0(self.response)
        transform_corners: np.ndarray = np.int0(self.transform_response)

        copy: np.ndarray = self.main_window.image.copy()
        transform_copy: np.ndarray = self.main_window.image_transformed.copy()
        
        for i, j in zip(corners, transform_corners):
            x, y = i.ravel()
            cv.circle(copy, (x, y), 3, 255, -1)
            x, y = j.ravel()
            cv.circle(transform_copy, (x, y), 3, 255, -1)
        
        self.main_window.update_no_transforms_label(copy)
        self.main_window.update_transforms_label(transform_copy)
    
    def update_main_window(self) -> None:
        if self.main_window.image is not None:
            self.response: np.ndarray = self.detector.get_response(self.main_window.image)
            self.transform_response: np.ndarray = self.detector.get_response(self.main_window.image_transformed)
            self.__set_features() 
        
    @pyqtSlot(int)
    def set_max_corners(self, max_corners: int) -> None:
        self.detector.max_corners = max_corners
        self.update_main_window()
            
    @pyqtSlot(int)
    def set_quality_level(self, quality_level: int) -> None:
        self.detector.quality_level = quality_level / 1000
        self.update_main_window()
        
    @pyqtSlot(int)
    def set_min_distance(self, min_distance: int) -> None:
        self.detector.min_distance = min_distance
        self.update_main_window()
        
    @pyqtSlot(int)
    def set_blocksize(self, blocksize: int) -> None:
        self.detector.blocksize = blocksize
        self.update_main_window()