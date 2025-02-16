#Useless, was used previously to attempt to map non-viable constituency name data onto existing region layers using centroids.

import json
import os
import geopandas as gpd
import pyproj
from shapely.geometry import shape, Point

# ✅ Paths
BOUNDARY_DIR = "/Users/supriyarai/Code/ge-o_map/Boundaries_JSON"
PCON_GEOJSON_FILE = "/Users/supriyarai/Code/ge-o_map/constituency_names.geojson"
OUTPUT_FILE = "/Users/supriyarai/Code/ge-o_map/merged_boundaries.json"

# ✅ Load constituency polygons
print("📌 Loading constituency boundaries...")
constituencies = gpd.read_file(PCON_GEOJSON_FILE)

if constituencies.empty:
    print("❌ Constituency data failed to load!")
    exit()

print(f"✅ Loaded {len(constituencies)} constituency polygons.")
print(f"✅ Constituency Data CRS: {constituencies.crs}")

# ✅ **Ensure constituency CRS is EPSG:4326**
if constituencies.crs is None or constituencies.crs.to_string() != "EPSG:4326":
    print("⚠️ Reprojecting constituency data to EPSG:4326...")
    constituencies = constituencies.to_crs("EPSG:4326")

# ✅ **Reproject to EPSG:3857 before computing centroids**
print("🔄 Reprojecting constituencies to EPSG:3857 for centroid calculations...")
constituencies = constituencies.to_crs("EPSG:3857")  # Convert first
constituencies["centroid"] = constituencies.geometry.centroid  # Now compute centroids

# ✅ **Check if centroids are correctly assigned**
if constituencies["centroid"].isnull().all():
    print("❌ ERROR: Constituency centroids are still NULL. Check geometry validity!")
    exit()

# ✅ Debugging: Show sample converted centroids
for i, row in constituencies.iterrows():
    print(f"🔍 Sample Constituency Centroid ({row['PCON24NM']}): {row['centroid']}")
    if i == 5:  # Print only first 5 to avoid clutter
        break

# ✅ Projection transformer: Convert EPSG:27700 → EPSG:4326
proj_transform = pyproj.Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

# ✅ Storage for merged data
merged_data = []
unmatched_boundaries = 0  # Track boundaries that fail to match

# ✅ Process each boundary file
processed = 0
for filename in os.listdir(BOUNDARY_DIR):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(BOUNDARY_DIR, filename)
    with open(file_path, "r") as f:
        boundary_data = json.load(f)

    # Extract boundary geometry
    geometry = shape(boundary_data["geometry"])

    # Compute centroid (EPSG:27700)
    centroid = geometry.centroid

    # 🔄 Convert centroid to EPSG:4326 (WGS84)
    lon, lat = proj_transform.transform(centroid.x, centroid.y)
    centroid = Point(lon, lat)  # Convert to GeoPandas format

    # 🔄 Reproject centroid to EPSG:3857 for **distance calculations**
    centroid_gdf = gpd.GeoDataFrame(geometry=[centroid], crs="EPSG:4326").to_crs("EPSG:3857")
    centroid_projected = centroid_gdf.geometry.iloc[0]

    # ✅ Find the closest constituency using nearest centroid
    distances = constituencies["centroid"].distance(centroid_projected)
    distances = distances.dropna()  # 🔥 Prevent NaN issues

    if not distances.empty:
        closest_idx = distances.idxmin()
        min_distance = distances.min()
        print(f"📏 Closest match: {constituencies.iloc[closest_idx]['PCON24NM']} at {min_distance:.2f} meters")

        if min_distance < 10000:  # Adjust threshold as needed
            constituency_name = constituencies.iloc[closest_idx]["PCON24NM"]
        else:
            constituency_name = "Unknown Constituency"
            unmatched_boundaries += 1  # Count failures
    else:
        print("❌ No valid constituency match found.")
        constituency_name = "Unknown Constituency"
        unmatched_boundaries += 1

    # ✅ Add name to JSON
    boundary_data["properties"]["constituency_name"] = constituency_name
    merged_data.append(boundary_data)

    processed += 1
    if processed % 500 == 0:
        print(f"🔄 Processed {processed} boundaries...")

# ✅ Save results
with open(OUTPUT_FILE, "w") as f:
    json.dump(merged_data, f, indent=4)

print(f"✅ Matching complete! {processed} boundaries assigned to constituencies.")
print(f"⚠️ Unmatched boundaries: {unmatched_boundaries} (These had no close constituency match)")
