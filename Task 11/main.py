from MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys
import numpy as np
import cv2 as cv
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.exec_()