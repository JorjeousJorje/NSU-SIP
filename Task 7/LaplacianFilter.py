from SobelFilter import SobelFilter, np
import cv2 as cv

class  LaplacianFilter(SobelFilter):
    def __init__(self, img: np.ndarray) -> None:
        super().__init__(img)

    def filter_image(self, img: np.ndarray) -> np.ndarray:
        img_laplace = cv.Laplacian(src=img, 
                                    ddepth=self.current_depth,
                                    ksize=2 * self.ksize + 1,
                                    delta=self.current_delta)
        return img_laplace

    def update_dx(self, value: int) -> np.ndarray:
        return self.noised_img
        
    def update_dy(self, value: int) -> np.ndarray:
        return self.noised_img
    
    