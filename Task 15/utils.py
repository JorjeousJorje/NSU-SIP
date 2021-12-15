import torch
import matplotlib.pyplot as plt
import numpy as np

from torch import Tensor


def evaluate_model(model, dataset):
    model.eval()
    
    with torch.no_grad():
        loader = torch.utils.data.DataLoader(dataset, batch_size=len(dataset))
        signals, labels = next(iter(loader))
        labels = labels.to(model.dummy_param)    
            
        classes, probas = model.predict(signals)
        total = len(dataset)
        return classes
        
        
def get_loaders(model_dataset, batch_size: int=100):
    total_count = len(model_dataset)
    train_count = int(0.7 * total_count)
    valid_count = int(0.2 * total_count)
    test_count = total_count - train_count - valid_count
    train_dataset, valid_dataset, test_dataset = torch.utils.data.random_split(
        model_dataset, (train_count, valid_count, test_count)
    )

    train_dataset_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )
    valid_dataset_loader = torch.utils.data.DataLoader(
        valid_dataset, batch_size=batch_size, shuffle=True
    )
    test_dataset_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False
    )

    dataloaders = {
        "train": train_dataset_loader,
        "val": valid_dataset_loader,
        "test": test_dataset_loader,
    }
    
    datasets = {
        "train": train_dataset,
        "val": valid_dataset,
        "test": test_dataset,
    }
    return dataloaders, datasets
