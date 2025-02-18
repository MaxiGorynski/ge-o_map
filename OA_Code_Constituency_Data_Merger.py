import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# ✅ Step 1: Load the OA Dataset (British Sign Language skills)
oa_dataset_path = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area-Full/UV211b - British Sign Language (BSL) skills by age (Full Geo).csv"
oa_df = pd.read_csv(oa_dataset_path, usecols=["OA_Code", "Latitude", "Longitude"])
print(f"✅ Loaded {len(oa_df)} rows from OA dataset.")

# ✅ Convert OA dataframe to a GeoDataFrame
oa_df["geometry"] = [Point(xy) for xy in zip(oa_df.Longitude, oa_df.Latitude)]
oa_gdf = gpd.GeoDataFrame(oa_df, geometry="geometry", crs="EPSG:4326")

# ✅ Step 2: Load the Constituency Dataset
constituency_path = "/Users/supriyarai/Code/ge-o_map/westminster-parliamentary-constituencies.geojson"
const_gdf = gpd.read_file(constituency_path)

# ✅ Ensure constituency dataset has the right CRS
const_gdf = const_gdf.to_crs("EPSG:4326")
print(f"✅ Loaded {len(const_gdf)} constituency boundaries.")

# ✅ Step 3: Perform a Spatial Join to Find Constituencies
merged_gdf = gpd.sjoin(oa_gdf, const_gdf, how="left", predicate="within")

# ✅ Step 4: Keep only the relevant columns
final_df = merged_gdf[["OA_Code", "Latitude", "Longitude", "PCON22NM"]]
final_df.rename(columns={"PCON22NM": "Constituency"}, inplace=True)

# ✅ Step 5: Save the final dataset
final_csv_path = "/oa_constituency_mapping.csv"
final_df.to_csv(final_csv_path, index=False)

print(f"✅ Final dataset with constituency data saved at: {final_csv_path}")
