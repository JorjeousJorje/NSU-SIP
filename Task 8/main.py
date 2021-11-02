from MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys
import cv2 as cv

if __name__ == '__main__':
    img = cv.imread(r'rub1.png')
    
    if img is not None: 
        resized = cv.resize(img, (1280, 800), interpolation = cv.INTER_AREA)
        app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
        window = MainWindow(resized) # Create an instance of our class
        window.show()
        app.exec_() # Start the application