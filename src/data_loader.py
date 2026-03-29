from torch.utils.data import DataLoader
from src.dataset import HouseDataset

def get_data_loaders(csv_path, img_dir, batch_size=32):

    dataset = HouseDataset(csv_path, img_dir)

    train_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    val_loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False
    )

    train_size = len(dataset)
    val_size = len(dataset)

    return train_loader, val_loader, train_size, val_size