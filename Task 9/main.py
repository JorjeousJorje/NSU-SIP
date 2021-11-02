from MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys
import numpy as np
        

# TODO: circles of transforms points (with their order)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.exec_()
