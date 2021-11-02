from MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys
import cv2 as cv
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    img = cv.imread(r'lenna.png')
    
    window = MainWindow(img)
    window.show()
    app.exec_()
    