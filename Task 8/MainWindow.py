from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QResizeEvent
import cv2 as cv
import numpy as np
from HoughCirclesDetector import HoughCirclesDetector

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, img: np.ndarray):
        super(MainWindow, self).__init__()
        uic.loadUi(r'ui/MainWindow.ui', self)
        
        self.image: np.ndarray = img
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.detector: HoughCirclesDetector = HoughCirclesDetector(gray)
        
        qimage = self.__get_qimage(img)
        self.img_label.setPixmap(qimage)
        
        self.__init_ui()
        
        
    def __init_ui(self) -> None:
        self.dp_slider.setValue(self.detector.dp)
        self.mindis_slider.setValue(self.detector.min_dist)
        self.param1_slider.setValue(self.detector.param1)
        self.param2_slider.setValue(self.detector.param2)
        self.minrad_slider.setValue(self.detector.min_rad)
        self.maxrad_slider.setValue(self.detector.max_rad)
    def __get_qimage(self, image) -> QImage:
        qimage = QImage(image, 
                        image.shape[1], 
                        image.shape[0], 
                        image.strides[0], 
                        QImage.Format_RGB888)
        
        qimage = qimage.rgbSwapped()
        return QPixmap.fromImage(qimage)
    
    
    def __draw_circles(self, cirles: np.ndarray) -> None:
        with_circles = self.image.copy()
        for item in cirles[0, :]:
            x, y, r = item[0], item[1], item[2]
            cv.circle(with_circles, (x, y), radius=r, color=(0, 255, 0), thickness=2)
            cv.circle(with_circles, (x, y), radius=2, color=(0, 0, 255), thickness=2)
        qimage = self.__get_qimage(with_circles)
        self.img_label.setPixmap(qimage)
            
    @pyqtSlot(int)
    def update_dp(self, dp: int) -> None:
        circles = self.detector.update_dp(dp)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
        
    @pyqtSlot(int)
    def update_min_dist(self, min_dist: int) -> None:
        circles = self.detector.update_min_dist(min_dist)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
    
    @pyqtSlot(int)
    def update_param1(self, param1: int) -> None:
        circles = self.detector.update_param1(param1)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
        
    @pyqtSlot(int)
    def update_param2(self, param2: int) -> None:
        circles = self.detector.update_param2(param2)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
        
    @pyqtSlot(int)
    def update_min_rad(self, min_rad: int) -> None:
        circles = self.detector.update_min_rad(min_rad)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
        
    @pyqtSlot(int)
    def update_max_rad(self, max_rad: int) -> None:
        circles = self.detector.update_max_rad(max_rad)
        if circles is None:
            return
        self.__draw_circles(circles.astype(np.uint16))
            