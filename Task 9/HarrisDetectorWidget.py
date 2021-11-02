from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
import cv2 as cv

from HarrisDetector import HarrisDetector


class HarrisDetectorWidget(QtWidgets.QWidget):
    def __init__(self, main_window) -> None:
        super(HarrisDetectorWidget, self).__init__()
        uic.loadUi(r'ui/HarrisWidget.ui', self)
        
        self.detector: HarrisDetector = HarrisDetector()
        
        self.transform_response: np.ndarray = None
        self.response: np.ndarray = None
        
        self.treshold: float = 0.001
        self.main_window = main_window
        
    def __set_corners(self) -> None:
        response: np.ndarray = cv.dilate(self.response, None)
        transform_response: np.ndarray = cv.dilate(self.transform_response, None)
        
        copy: np.ndarray = self.main_window.image.copy()
        transform_copy: np.ndarray = self.main_window.image_transformed.copy()
        
        copy[response > self.treshold * response.max()] = [0, 255, 0]
        transform_copy[transform_response > self.treshold * response.max()] = [0, 255, 0]
        
        self.main_window.update_no_transforms_label(copy)
        self.main_window.update_transforms_label(transform_copy)
        
    @pyqtSlot(int)    
    def set_treshold(self, treshold: int) -> None:
        self.treshold = treshold / 1000
        if self.response is not None:
            self.__set_corners()
    
    def update_main_window(self) -> None:
        if self.main_window.image is not None:
            self.response: np.ndarray = self.detector.get_response(self.main_window.image)
            self.transform_response: np.ndarray = self.detector.get_response(self.main_window.image_transformed)
            self.__set_corners() 

    @pyqtSlot(int)
    def set_blocksize(self, blocksize: int) -> None:
        self.detector.blocksize = blocksize
        self.update_main_window()
        
    @pyqtSlot(int)
    def set_ksize(self, ksize: int) -> None:
        self.detector.ksize = 2 * ksize + 1
        self.update_main_window()
        
    @pyqtSlot(int)
    def set_k(self, k: int) -> None:
        self.detector.k = k / 100
        self.update_main_window()