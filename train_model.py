import os
import pandas as pd
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import r2_score, mean_absolute_error
import json

BASE_PATH = "Houses-dataset/Houses Dataset"

# ================= LOAD =================
cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
df = pd.read_csv(os.path.join(BASE_PATH, "HousesInfo.txt"), sep=" ", header=None, names=cols)

# ================= LOAD LAT/LON =================
with open("models/latlon_map.json") as f:
    latlon_map = json.load(f)

df["lat"] = df["zipcode"].apply(lambda z: latlon_map.get(str(int(z)), [0,0])[0])
df["lon"] = df["zipcode"].apply(lambda z: latlon_map.get(str(int(z)), [0,0])[1])

# ================= FEATURE ENGINEERING =================
df["density"] = df["price"] / (df["area"] + 1)

# Normalize lat/lon
df["lat"] = (df["lat"] - df["lat"].mean()) / df["lat"].std()
df["lon"] = (df["lon"] - df["lon"].mean()) / df["lon"].std()

# ================= NORMALIZATION =================
scale = {
    "price_max": float(df["price"].max()),
    "area_max": float(df["area"].max()),
    "bed_max": float(df["bedrooms"].max()),
    "bath_max": float(df["bathrooms"].max()),
}

df["price"] /= scale["price_max"]
df["bedrooms"] /= scale["bed_max"]
df["bathrooms"] /= scale["bath_max"]
df["area"] /= scale["area_max"]

os.makedirs("models", exist_ok=True)
with open("models/price_scale.json", "w") as f:
    json.dump(scale, f)

train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# ================= TRANSFORM =================
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])

# ================= DATASET =================
class HouseDataset(Dataset):
    def __init__(self, df):
        self.df = df.copy()
        self.df["id"] = self.df.index
        self.valid_rows = []

        for _, row in self.df.iterrows():
            hid = str(int(row["id"]) + 1).zfill(5)
            paths = [
                os.path.join(BASE_PATH, f"{hid}_{t}.jpg")
                for t in ["bedroom","bathroom","kitchen","front"]
            ]
            if all(os.path.exists(p) for p in paths):
                self.valid_rows.append(row)

    def __len__(self):
        return len(self.valid_rows)

    def __getitem__(self, idx):
        row = self.valid_rows[idx]
        hid = str(int(row["id"]) + 1).zfill(5)

        imgs = []
        for t in ["bedroom","bathroom","kitchen","front"]:
            path = os.path.join(BASE_PATH, f"{hid}_{t}.jpg")
            img = Image.open(path).convert("RGB")
            imgs.append(transform(img))

        image = torch.cat(imgs, dim=0)

        features = torch.tensor([
            row["bedrooms"],
            row["bathrooms"],
            row["area"],
            row["lat"],
            row["lon"]
        ], dtype=torch.float32)
        price = torch.tensor(row["price"], dtype=torch.float32)

        return image, features, price

train_loader = DataLoader(HouseDataset(train_df), batch_size=16, shuffle=True)
test_loader = DataLoader(HouseDataset(test_df), batch_size=16)

# ================= MODEL =================
class Model(nn.Module):
    def __init__(self):
        super().__init__()

        resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        for param in resnet.parameters():
            param.requires_grad = False

        for param in resnet.layer4.parameters():
            param.requires_grad = True

        self.cnn = nn.Sequential(*list(resnet.children())[:-1])

        self.img_fc = nn.Linear(512, 64)

        self.tab_fc = nn.Sequential(
            nn.Linear(5, 64),
            nn.ReLU()
        )

        self.fc = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, img, feat):
        B = img.size(0)
        imgs = img.view(B, 4, 3, 224, 224)

        feats = []
        for i in range(4):
            x = self.cnn(imgs[:, i]).view(B, -1)
            feats.append(x)

        img_feat = torch.stack(feats).mean(dim=0)
        img_feat = self.img_fc(img_feat)

        tab_feat = self.tab_fc(feat)

        x = torch.cat([img_feat, tab_feat], dim=1)
        return self.fc(x)

# ================= TRAIN =================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Model().to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
loss_fn = nn.MSELoss()

for epoch in range(30):
    model.train()
    total_loss = 0

    for img, feat, price in train_loader:
        img, feat, price = img.to(device), feat.to(device), price.to(device)

        pred = model(img, feat).squeeze()
        loss = loss_fn(pred, price)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1} Loss: {total_loss:.4f}")

torch.save(model.state_dict(), "models/best_model.pth")

# ================= EVAL =================
model.eval()
preds, targets = [], []

with torch.no_grad():
    for img, feat, price in test_loader:
        img, feat = img.to(device), feat.to(device)
        p = model(img, feat).squeeze().cpu().numpy()

        preds.extend(p)
        targets.extend(price.numpy())

print("R2:", r2_score(targets, preds))
print("MAE:", mean_absolute_error(targets, preds))