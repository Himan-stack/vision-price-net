import os
from flask import Flask, request, render_template
import json
import joblib
import pandas as pd
from PIL import Image

app = Flask(__name__)

print("Starting app...")

# ================= LOAD LAT/LON =================
with open("models/latlon_map.json") as f:
    latlon_map = json.load(f)

# ================= LOAD MODEL =================
try:
    print("Loading XGBoost model...")
    xgb_model = joblib.load("models/xgb_model.pkl")
    print("XGBoost model loaded ✅")
except Exception as e:
    print("MODEL LOAD ERROR:", e)

with open("models/price_scale.json") as f:
    scale = json.load(f)

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    # ===== INPUT =====
    try:
        bedrooms = float(request.form["bedrooms"])
        bathrooms = float(request.form["bathrooms"])
        area = float(request.form["area"])
        zipcode = int(request.form["location"])
    except:
        return render_template("index.html", result="Invalid input")

    # ===== BASIC VALIDATION =====
    if bedrooms <= 0 or bathrooms <= 0 or area <= 0:
        return render_template("index.html", result="Invalid values")

    # ===== PREDICTION =====
    xgb_features = pd.DataFrame([{
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "area": area
    }])

    try:
        price = xgb_model.predict(xgb_features)[0]
    except Exception as e:
        return render_template("index.html", result=f"Prediction error: {e}")

    # ===== OUTPUT =====
    lower = price * 0.9
    upper = price * 1.1

    return render_template(
        "index.html",
        result=f"Predicted Price: ${price:,.0f}",
        confidence=90,
        price_range=f"${lower:,.0f} - ${upper:,.0f}",
        location=zipcode
    )

# ================= RUN =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)