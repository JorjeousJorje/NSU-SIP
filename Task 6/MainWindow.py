import re, os, sys

from itertools import product
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QSize, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from tools import *
import numpy as np
import cv2 as cv

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi(r'ui/MainWindow.ui', self)
        
        self.image: np.ndarray = None
        self.gray_image: np.ndarray = None
        self.contours: list = None
        self.hull: list = None
        self.image_area: float = None
        
        self.low_threshold = 100
        self.max_threshold = 200
        
        self.len_approx_to_figure = {   3: "Triangle",
                                        5: "Pentagon",
                                        6: "Hexagon" }
        
    @staticmethod
    def __get_qimage(image) -> QImage:
        
        format = QImage.Format_RGB888
        
        if len(image.shape) < 3:
            format = QImage.Format_Grayscale8
        
        qimage = QImage(image, 
                        image.shape[1], 
                        image.shape[0], 
                        image.strides[0], 
                        format)
        
        qimage = qimage.rgbSwapped()
        return QPixmap.fromImage(qimage)
    
    
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
        
        self.init_variables()
    
    def update_img_label(self, image: np.ndarray) -> None:
        qimage = MainWindow.__get_qimage(image)
        self.img_label.setPixmap(qimage)
        
    def __resize_to_label(self, image: np.ndarray) -> None:
        label_size: QSize = self.img_label.size()
        dim: tuple[int, int] = (label_size.width(), label_size.height())
        self.image: np.ndarray = cv.resize(src=image, dsize=dim, interpolation=cv.INTER_AREA)
    
    
    def get_area_class(self, area_ratio):
        size = 'large'
        if area_ratio >= 0.6:
            size = 'large'
        elif 0.2 <= area_ratio < 0.6:
            size = 'medium'
        else:
            size = 'small'

        return size
    

    def get_shape_class(self):
        approx = self.approx_contour(self.hull)
        num_of_lines = len(approx)
        if num_of_lines < 7:
            if num_of_lines == 4:
                area = cv.contourArea(self.hull)
                (x, y), radius = cv.minEnclosingCircle(self.hull)
                perimeter = cv.arcLength(self.hull, closed=True)
                possible_square_area = 2 * (radius ** 2)
                
                if perimeter ** 2 > 16 * possible_square_area:
                    shape_name = "Square"
                else:
                    shape_name = "Rectangle"
            else:
                try:
                    shape_name = self.len_approx_to_figure[num_of_lines]
                except:
                    shape_name = "Cannot predict"
        else:
            area = cv.contourArea(self.hull)
            _, radius = cv.minEnclosingCircle(self.hull)
            approximate_circle_area = np.pi * (radius ** 2)
            
            if 0.9 * approximate_circle_area <= area <= 1.1 * approximate_circle_area:
                shape_name = "Circle"
            else:
                shape_name = "Ellipse"
        
        return shape_name
        
        
    def init_variables(self) -> None:
        self.__resize_to_label(self.image)
        

        self.image_area = self.image.shape[0] * self.image.shape[1]
        self.area_tresh = 0.002
        self.image = cv.blur(self.image, ksize=(3, 3))
        
        self.max_ratio = -1
        for i, j in product(range(10), range(10)):
            t1 = np.int0(i * 255 / 10)
            t2 = np.int0(j * 255 / 10)

            self.set_hull()
            area = cv.contourArea(self.hull)
            area_ratio = area / self.image_area

            if area_ratio > self.max_ratio:
                self.max_ratio = area_ratio
                self.low_threshold = t1
                self.max_threshold = t2
        
        self.set_hull()
        
        x, y, w, h = cv.boundingRect(self.hull)
        area = w * h
        area_ratio = area / self.image_area
        area_class = self.get_area_class(area_ratio)
        shape_class = self.get_shape_class()
        
        current_image = self.image.copy()
        
        font = cv.FONT_HERSHEY_SIMPLEX
        fontScale = 1.5
        fontColor = (255, 20, 156)
        thickness = 3
        x, y, w, h = cv.boundingRect(self.hull)
        
        persent_text = f"area: {area_ratio * 100:.1f}%"
        cv.drawContours(current_image, [self.hull], -1, (255, 255, 0), 3, 1)
        # cv.rectangle(current_image, (x, y), (x + w, y + h), (255, 255, 0), 1)
        cv.putText(current_image, persent_text, (x, y), font, fontScale, fontColor, thickness)
        cv.putText(current_image, f"object size: {area_class}", (x, y + 45), font, fontScale, fontColor, thickness)
        cv.putText(current_image, f"object type: {shape_class}", (x, y + 90), font, fontScale, (15, 20, 255), thickness)
        self.update_img_label(current_image)
        
    def set_hull(self):
        self.contours, _ = self.detect_contours()
        self.filter_contours()
        
        self.total_contour = np.vstack(self.contours)
        self.hull = cv.convexHull(self.total_contour)

    def detect_contours(self):
        self.thresh = cv.Canny(self.image, self.low_threshold, self.max_threshold, L2gradient=True)
        contours, hierarchy = cv.findContours(self.thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy
    
    def approx_contour(self, cntr):
        perimeter = cv.arcLength(cntr, True)
        approx = cv.approxPolyDP(cntr, 0.02 * perimeter, True)
        return approx

    def filter_contours(self):
        filtered = []
        for _, c in enumerate(self.contours):
            hull = cv.convexHull(c)
            area = cv.contourArea(hull)
            
            approx = self.approx_contour(c)
            
            if area / self.image_area > self.area_tresh:
                filtered.append(c)
                
        self.contours = filtered   
            
        
       
    @pyqtSlot(int) 
    def on_update(self, value: int):
        pass
        
    @pyqtSlot(int)
    def update_contours(self, value: int) -> None:
        pass
        
        
      
      
        
        
    