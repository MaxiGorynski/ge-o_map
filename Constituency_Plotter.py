import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape

# ✅ Load CSV (Include "Geo Shape" for full constituency boundaries)
df = pd.read_csv("/Users/supriyarai/Code/ge-o_map/westminster-parliamentary-constituencies.csv",
                 usecols=["PCON22NM", "Geo Shape", "LONG", "LAT"])

# ✅ Convert "Geo Shape" from JSON to Shapely geometry
df["geometry"] = df["Geo Shape"].apply(lambda x: shape(json.loads(x)) if isinstance(x, str) else None)

# ✅ Convert DataFrame to GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# ✅ Drop the old text-based "Geo Shape" column (now converted)
gdf.drop(columns=["Geo Shape"], inplace=True)

# ✅ Export as GeoJSON with correct format
geojson_path = "/Users/supriyarai/Code/ge-o_map/westminster-parliamentary-constituencies.geojson"
gdf.to_file(geojson_path, driver="GeoJSON")

print(f"✅ GeoJSON successfully saved: {geojson_path}")
