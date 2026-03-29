import torch
from flask import Flask, request, render_template
from PIL import Image
import torchvision.transforms as transforms
import torch.nn as nn
from torchvision import models
import json
import joblib
import pandas as pd

app = Flask(__name__)

# ================= LOAD LAT/LON =================
with open("models/latlon_map.json") as f:
    latlon_map = json.load(f)

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

# ================= LOAD MODELS =================
device = torch.device("cpu")

dl_model = Model().to(device)
dl_model.load_state_dict(torch.load("models/best_model.pth", map_location=device))
dl_model.eval()

xgb_model = joblib.load("models/xgb_model.pkl")

with open("models/price_scale.json") as f:
    scale = json.load(f)

price_max = scale["price_max"]

# ================= TRANSFORM =================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ================= ROUTES =================
@app.route("/predict")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    # ===== GET IMAGES =====
    files = [
        request.files.get("image1"),
        request.files.get("image2"),
        request.files.get("image3"),
        request.files.get("image4"),
    ]

    if any(f is None for f in files):
        return render_template("index.html", result="Upload all 4 images")

    # ===== GET INPUTS =====
    try:
        bedrooms = float(request.form["bedrooms"])
        bathrooms = float(request.form["bathrooms"])
        area = float(request.form["area"])
        zipcode = int(request.form["location"])
    except:
        return render_template("index.html", result="Invalid inputs")

    # ===== LAT/LON =====
    lat, lon = latlon_map.get(str(zipcode), (0, 0))

    # ===== NORMALIZE FOR DL =====
    bed_n = bedrooms / scale["bed_max"]
    bath_n = bathrooms / scale["bath_max"]
    area_n = area / scale["area_max"]

    # ===== PROCESS IMAGES =====
    images = []
    for file in files:
        img = Image.open(file).convert("RGB")
        img = transform(img)
        images.append(img)

    image = torch.stack(images).unsqueeze(0)

    features_dl = torch.tensor(
        [[bed_n, bath_n, area_n, lat, lon]],
        dtype=torch.float32
    )

    # ===== DL PREDICTION =====
    with torch.no_grad():
        dl_pred = dl_model(image, features_dl).item()

    dl_price = dl_pred * price_max

    # ===== XGB PREDICTION (ONLY 3 FEATURES) =====
    xgb_features = pd.DataFrame([{
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "area": area
    }])

    xgb_price = xgb_model.predict(xgb_features)[0]

    # ===== ENSEMBLE =====
    final_price = 0.3 * dl_price + 0.7 * xgb_price

    # ===== CONFIDENCE =====
    error_ratio = abs(dl_price - xgb_price) / final_price
    confidence = max(60, 100 - (error_ratio * 100))
    confidence = round(confidence, 2)

    # ===== RANGE =====
    lower = final_price * 0.9
    upper = final_price * 1.1

    return render_template(
        "index.html",
        result=f"Predicted Price: ${final_price:,.0f}",
        confidence=confidence,
        price_range=f"${lower:,.0f} - ${upper:,.0f}",
        location=zipcode
    )

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)