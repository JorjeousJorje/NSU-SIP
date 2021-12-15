from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
import cv2 as cv

from TomachiDetector import TomachiDetector


class TomachiDetectorWidget(QtWidgets.QWidget):
    def __init__(self, main_window) -> None:
        super(TomachiDetectorWidget, self).__init__()
        uic.loadUi(r'ui/TomachiWidget.ui', self)
        
        
        self.main_window = main_window
    

    
    def __resize_to_label(self, image: np.ndarray):
        label_size = self.img_label.size()
        dim: tuple[int, int] = (label_size.width(), label_size.height())
        return cv.resize(src=image, dsize=dim, interpolation=cv.INTER_AREA)
        
    @pyqtSlot()
    def show_features(self) -> None:
        
        if self.main_window.image is not None:
            img1 = self.main_window.image.copy()
            img2 = self.main_window.image_transformed.copy()
            
            
            src = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            needle = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
            
            MAX_FEATURES = 500
            orb = cv.ORB_create(MAX_FEATURES)
            kp1, des1 = orb.detectAndCompute(src, None)
            kp2, des2 = orb.detectAndCompute(needle, None)
            bf = cv.BFMatcher(cv.NORM_HAMMING2, crossCheck=True)

            matches = bf.match(des2, des1)
            matches = sorted(matches, key=lambda x: x.distance)
            
            GOOD_MATCH_PERCENT = 0.15
            numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
            matches = matches[: numGoodMatches]

            with_mathces = cv.drawMatches(img2, kp2, img1, kp1, matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
       
            qimage = self.main_window.get_qimage(self.__resize_to_label(with_mathces))
            self.img_label.setPixmap(qimage)