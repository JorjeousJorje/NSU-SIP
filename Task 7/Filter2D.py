from FilterType import FilterType, np
import cv2 as cv


class Filter2D(FilterType):
    def __init__(self, img: np.ndarray) -> None:
        super().__init__(img)
        self.depths: list = [-1,  cv.CV_32F, cv.CV_64F]
        self.kernels = [np.ones((5, 5)), 
                        np.array([[0.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 0.0]]),
                        np.array([[0.0, -1.0, 0.0], [-1.0, 5.0, -1.0], [0.0, -1.0, 0.0]]),
                        np.array([[-1.0, -1.0], [2.0, 2.0], [-1.0, -1.0]])]
        self.__normalize_kernels()
        
        self.current_kernel: np.ndarray = self.kernels[0]
        self.current_depth: int = self.depths[0]
        self.current_delta: float = 0.0
        
        
    def __normalize_kernels(self) -> None:
        
        for kernel in self.kernels:
            kernel /= np.sum(kernel) if np.sum(kernel) != 0 else 1
            
    def filter_image(self, img: np.ndarray) -> np.ndarray:
        
        img_filtered = cv.filter2D(src=img,
                                ddepth=self.current_depth,
                                kernel=self.current_kernel, 
                                anchor=(-1, -1),
                                delta=self.current_delta)
        return img_filtered
            
    def update_kernel(self, value: int) -> np.ndarray:
        self.current_kernel = self.kernels[value]
        return self.filter_image(self.noised_img)
        
    def update_depth(self, value: int) -> np.ndarray:
        self.current_depth = self.depths[value]
        return self.filter_image(self.noised_img)
    
    def update_delta(self, value: int) -> np.ndarray:
        self.current_delta = float(value / 100)
        return self.filter_image(self.noised_img)
    
    def reset_params(self) -> None:
        self.current_kernel: np.ndarray = self.kernels[0]
        self.current_depth: int = self.depths[0]
        self.current_delta: float = 0.0
        self.ksize = 0