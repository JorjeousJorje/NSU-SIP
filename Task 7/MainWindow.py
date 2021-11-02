from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import numpy as np


from FilterParametersWidget import FilterParametersWidget
from Filter2DParametersWidget import Filter2DParametersWidget
from SobelParametersWidget import SobelParametersWidget
from GaussFilter import GaussFilter
from MedianFilter import MedianFilter
from Filter2D import Filter2D
from SobelFilter import SobelFilter
from LaplacianFilter import LaplacianFilter

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, img: np.ndarray):
        super(MainWindow, self).__init__()
        uic.loadUi(r'ui/MainWindow.ui', self)
        
        self.image: np.ndarray = img
        self.widgets = {'gauss' : FilterParametersWidget(GaussFilter(self.image), self),
                        'median' : FilterParametersWidget(MedianFilter(self.image), self),
                        'filter2d' : Filter2DParametersWidget(Filter2D(self.image), self),
                        'sobel' : SobelParametersWidget(SobelFilter(self.image), self),
                        'laplace' : SobelParametersWidget(LaplacianFilter(self.image), self)}
        
        
        self.current_widget = None
        qimage = self.__get_qimage(self.image)
        self.original_image_label.setPixmap(qimage)
        self.filtered_image_label.setPixmap(qimage)
        
        self.add_noise_button.clicked.connect(self.__add_noise)
        self.remove_noise_button.clicked.connect(self.__remove_noise)
        
    
    def __get_qimage(self, image) -> QImage:
        qimage = QImage(image, 
                        image.shape[1], 
                        image.shape[0], 
                        image.strides[0], 
                        QImage.Format_RGB888)
        
        qimage = qimage.rgbSwapped()
        return QPixmap.fromImage(qimage)
        
    def __add_noise(self) -> None:
        noise = None
        if self.normal_checkbox.isChecked():
            noise = np.random.normal(self.mean_spinbox.value(), 
                                     self.std_spinbox.value(), 
                                     self.image.shape)
        elif self.uniform_checkbox.isChecked():
            noise = np.random.uniform(self.low_spinbox.value(), 
                                      self.high_spinbox.value(), 
                                      self.image.shape)
        elif self.normal_checkbox.isChecked() and self.uniform_checkbox.isChecked():
            noise = np.random.normal(self.mean_spinbox.value(), 
                                     self.std_spinbox.value(), 
                                     self.image.shape)
            noise += np.random.uniform(self.low_spinbox.value(), 
                                      self.high_spinbox.value(), 
                                      self.image.shape)
        
        if noise is not None:
            clipped = np.clip(self.image + noise, 0, 255)
            
            if self.current_widget is not None:
                self.current_widget.filter.set_noised_image(clipped.astype(self.image.dtype))
            
            qimage = self.__get_qimage(clipped.astype(self.image.dtype))
            self.filtered_image_label.setPixmap(qimage)
            self.original_image_label.setPixmap(qimage)
        
    def __remove_noise(self) -> None:
        qimage = self.__get_qimage(self.image)
        
        if self.current_widget is not None:
            self.current_widget.filter.set_noised_image(self.image)
            self.current_widget.filter.reset_params()
        
        self.filtered_image_label.setPixmap(qimage)
        self.original_image_label.setPixmap(qimage)
        
    def set_filtered_img(self, img: np.ndarray):
        qimage = self.__get_qimage(img.astype(self.image.dtype))
        self.filtered_image_label.setPixmap(qimage)
        
    @pyqtSlot()   
    def show_gauss_filter_widget(self):
        if self.current_widget is not None:
            self.current_widget.close()
        self.current_widget = self.widgets['gauss']
        self.current_widget.setWindowTitle('gauss')
        self.current_widget.slider_name_label_2.setText("sigma_x")
        self.current_widget.slider_name_label_3.setText("sigma_y")
        self.current_widget.show()
        
    @pyqtSlot()   
    def show_median_filter_widget(self):
        if self.current_widget is not None:
            self.current_widget.close()
        self.current_widget = self.widgets['median']
        self.current_widget.setWindowTitle('median')
        self.current_widget.slider_name_label_2.setText("")
        self.current_widget.slider_name_label_3.setText("")
        self.current_widget.show()
        
    @pyqtSlot()   
    def show_filter2d_widget(self):
        if self.current_widget is not None:
            self.current_widget.close()
        self.current_widget = self.widgets['filter2d']
        self.current_widget.setWindowTitle('filter2d')
        self.current_widget.show()
    
    @pyqtSlot()   
    def show_sobel_widget(self):
        if self.current_widget is not None:
            self.current_widget.close()
        self.current_widget = self.widgets['sobel']
        self.current_widget.setWindowTitle('sobel')
        self.current_widget.show()
        
    @pyqtSlot()   
    def show_laplace_widget(self):
        if self.current_widget is not None:
            self.current_widget.close()
        self.current_widget = self.widgets['laplace']
        self.current_widget.setWindowTitle('laplace')
        self.current_widget.show()
      
        
        
        
