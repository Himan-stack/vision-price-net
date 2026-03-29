import pandas as pd
from xgboost import XGBRegressor
import joblib
import numpy as np
import json
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import cross_val_score

# =========================
# Load dataset
# =========================
columns = ["bedrooms","bathrooms","area","zipcode","price"]
df = pd.read_csv("Houses-dataset/HousesInfo.txt", sep=r"\s+", header=None, names=columns)

df = df.drop_duplicates()

# =========================
# Add small noise (prevents overfitting)
# =========================
df["area"] = df["area"] * (1 + np.random.normal(0, 0.05, len(df)))
df["bedrooms"] = df["bedrooms"] + np.random.randint(-1, 2, len(df))
df["bathrooms"] = df["bathrooms"] + np.random.randint(-1, 2, len(df))

df["bedrooms"] = df["bedrooms"].clip(lower=1)
df["bathrooms"] = df["bathrooms"].clip(lower=1)

# =========================
# Features
# =========================
X = df[["bedrooms","bathrooms","area"]]
y = df["price"]

# =========================
# Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Model
# =========================
model = XGBRegressor(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.03,
    subsample=0.7,
    colsample_bytree=0.7,
    reg_alpha=5,
    reg_lambda=5,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# Evaluation
# =========================
preds = model.predict(X_test)

print("XGB R2:", r2_score(y_test, preds))
print("XGB MAE:", mean_absolute_error(y_test, preds))

# =========================
# Cross Validation
# =========================
scores = cross_val_score(model, X, y, cv=5, scoring="r2")
print("Cross-val R2:", scores.mean())

# =========================
# Plot
# =========================
xgb.plot_importance(model)
plt.show()

# =========================
# Save
# =========================
joblib.dump(model, "models/xgb_model.pkl")

print("✅ XGBoost trained correctly!")