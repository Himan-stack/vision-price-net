import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class HouseDataset(Dataset):

    def __init__(self, csv_path, img_dir):

        self.data = pd.read_csv(csv_path)
        self.img_dir = img_dir

        self.transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        row = self.data.iloc[idx]

        img_path = os.path.join(self.img_dir, row["image"])

        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)

        features = torch.tensor([
            row["bedrooms"],
            row["bathrooms"],
            row["area"]
        ], dtype=torch.float32)

        price = torch.tensor(row["price"], dtype=torch.float32)

        return image, features, price