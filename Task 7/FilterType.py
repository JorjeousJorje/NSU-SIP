import numpy as np
from abc import ABC
from abc import abstractmethod

class FilterType(ABC):
    
    def __init__(self, img) -> None:
        self.ksize: int = 0
        self.noised_img: np.ndarray = img
        
    @abstractmethod
    def filter_image(self, img: np.ndarray) -> np.ndarray:
        pass
    
    def set_noised_image(self, noised_img: np.ndarray):
         self.noised_img = noised_img
         
    def update_ksize(self, ksize: int) -> np.ndarray:
        self.ksize = ksize
        return self.filter_image(self.noised_img)
    
    @abstractmethod
    def reset_params(self) -> None:
        pass
    