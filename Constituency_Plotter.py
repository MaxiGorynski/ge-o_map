import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# ✅ Load only the necessary columns
df = pd.read_csv("/Users/supriyarai/Code/ge-o_map/westminster-parliamentary-constituencies.csv", usecols=["PCON22NM", "LONG", "LAT"])

# ✅ Convert to GeoPandas
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["LONG"], df["LAT"]), crs="EPSG:4326")

# ✅ Plot the constituency locations
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color="red", markersize=5, alpha=0.7)

plt.title("Westminster Parliamentary Constituency Centroids")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
