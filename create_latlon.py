import pandas as pd
import json

# Load your dataset
df = pd.read_csv(
    "Houses-dataset/HousesInfo.txt",
    sep=" ",
    header=None,
    names=["bedrooms", "bathrooms", "area", "zipcode", "price"]
)

# Load real ZIP dataset

zip_df = pd.read_csv("simplemaps_uszips_basicv1.94/uszips.csv")

# Create mapping
latlon_map = {}

for zipc in df["zipcode"].unique():
    match = zip_df[zip_df["zip"] == zipc]
    
    if not match.empty:
        lat = float(match.iloc[0]["lat"])
        lon = float(match.iloc[0]["lng"])
        latlon_map[int(zipc)] = [lat, lon]

# Save
with open("models/latlon_map.json", "w") as f:
    json.dump(latlon_map, f, indent=4)

print("✅ Real lat/lon map created!")