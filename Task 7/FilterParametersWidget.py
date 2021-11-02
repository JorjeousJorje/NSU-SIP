from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
import numpy as np

class FilterParametersWidget(QtWidgets.QWidget):
    def __init__(self, _filter, main_window):
        super(FilterParametersWidget, self).__init__()
        uic.loadUi(r'ui/FilterParameters.ui', self)
        
        
        self.main_window = main_window
        self.filter = _filter
        
        self.__init_ui()
        
        
    def __init_ui(self) -> None:
        self.spin_to.setValue(self.ksize_slider.maximum())
        self.spin_to_4.setValue(self.second_parameter_slider.maximum())
        self.spin_to_5.setValue(self.third_parameter_slider.maximum())
        
        self.spin_from.setValue(self.ksize_slider.minimum())
        self.spin_from_2.setValue(self.second_parameter_slider.minimum())
        self.spin_from_3.setValue(self.third_parameter_slider.minimum())
        
        self.ksize_lcd.display(self.ksize_slider.value())
        
        
    @pyqtSlot()
    def set_max_ksize_slider(self) -> None:
        self.ksize_slider.setMaximum(self.spin_to.value())
        
    @pyqtSlot()
    def set_min_ksize_slider(self) -> None:
        self.ksize_slider.setMinimum(self.spin_from.value())
        
    @pyqtSlot()
    def set_max_second_slider(self) -> None:
        self.second_parameter_slider.setMaximum(self.spin_to_4.value())
        
    @pyqtSlot()
    def set_min_second_slider(self) -> None:
        self.second_parameter_slider.setMinimum(self.spin_from_2.value())
        
    @pyqtSlot()
    def set_max_third_slider(self) -> None:
        self.third_parameter_slider.setMaximum(self.spin_to_5.value())
        
    @pyqtSlot()
    def set_min_third_slider(self) -> None:
        self.third_parameter_slider.setMinimum(self.spin_from_3.value())
        
    @pyqtSlot()
    def on_change(self) -> None:
        sender = self.sender()
        method_name = 'update_'
        
        if sender is self.ksize_slider:
            method_name += 'ksize'
            method = getattr(self.filter, method_name)
            self.main_window.set_filtered_img(method(self.ksize_slider.value()))
            
        elif sender is self.second_parameter_slider:
            method_name += self.slider_name_label_2.text()
            if method_name != 'update_':
                method = getattr(self.filter, method_name)
                self.main_window.set_filtered_img(method(self.second_parameter_slider.value()))
        elif sender is self.third_parameter_slider:
            method_name += self.slider_name_label_3.text()
            if method_name != 'update_':
                method = getattr(self.filter, method_name)
                self.main_window.set_filtered_img(method(self.third_parameter_slider.value()))
