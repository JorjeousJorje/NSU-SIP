from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
from Filter2D import Filter2D

class Filter2DParametersWidget(QtWidgets.QWidget):
    def __init__(self, _filter: Filter2D, main_window):
        super(Filter2DParametersWidget, self).__init__()
        uic.loadUi(r'ui/Filter2DParametersWidget.ui', self)
        
        
        self.main_window = main_window
        self.filter = _filter
        self.__init_ui()
        
    def __init_ui(self):
        self.kernels_slider.setMaximum(len(self.filter.kernels) - 1)
        self.type_slider.setMaximum(len(self.filter.depths) - 1)
        
    @pyqtSlot()
    def on_change(self) -> None:
        sender = self.sender()
        method_name = 'update_'
        
        if sender is self.kernels_slider:
            method_name += 'kernel'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.kernels_slider.value()))
            
        elif sender is self.type_slider:
            method_name += 'depth'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.type_slider.value()))
        
        elif sender is self.delta_slider:
            method_name += 'delta'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.delta_slider.value()))