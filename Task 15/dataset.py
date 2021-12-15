import os
import torch
import numpy as np
import cv2 as cv

from PIL import Image
from torch import Tensor
from torch.utils.data import Dataset



class BadgerDataset(Dataset):
    def __init__(self, train_folder: str, transforms = None):
        self.train_folder = train_folder
        self.dirlist = os.listdir(train_folder)
        self.transforms = transforms
        
    def __len__(self):
        return len(self.dirlist)
    
    
    def __getitem__(self, index) -> tuple[Tensor, int]:        
        image = Image.open(self.train_folder + os.sep + self.dirlist[index])
        
        label = None
        
        if "badger" in self.dirlist[index]:
            label = 1
        else:
            label = 0
        
        if self.transforms:
            image = self.transforms(image)
        
        
        return image, label


