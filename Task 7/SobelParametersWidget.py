from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np
from SobelFilter import SobelFilter

class SobelParametersWidget(QtWidgets.QWidget):
    def __init__(self, _filter: SobelFilter, main_window):
        super(SobelParametersWidget, self).__init__()
        uic.loadUi(r'ui/SobelParametersWidget.ui', self)
        
        
        self.main_window = main_window
        self.filter = _filter
        self.__init_ui()
        
    def __init_ui(self):
        self.type_slider.setMaximum(len(self.filter.depths) - 1)
        self.dx_slider.setMaximum(30)
        self.dy_slider.setMaximum(30)
        
    @pyqtSlot()
    def on_change(self) -> None:
        sender = self.sender()
        method_name = 'update_'
        
        if sender is self.ksize_slider:
            method_name += 'ksize'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.ksize_slider.value()))
            
        elif sender is self.type_slider:
            method_name += 'depth'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.type_slider.value()))
        
        elif sender is self.delta_slider:
            method_name += 'delta'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.delta_slider.value()))
            
        elif sender is self.dx_slider:
            method_name += 'dx'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.dx_slider.value()))
            
        elif sender is self.dy_slider:
            method_name += 'dy'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.dy_slider.value()))