import geopandas as gpd
import pandas as pd
import os
from shapely.validation import make_valid

# Paths
csv_folder = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area"
gml_file = "CEN2022_OA.xml"

# Load GeoDataFrame
geodata = gpd.read_file(gml_file)

#Initialise GeoDataFrame
geo_df = gpd.GeoDataFrame()

# Inspect for duplicate columns
if geodata.columns.duplicated().any():
    print("Duplicate columns detected in GeoDataFrame:")
    print(geodata.columns[geodata.columns.duplicated()])
    # Remove duplicate columns
    geodata = geodata.loc[:, ~geodata.columns.duplicated()]

# Rename the correct 'CEN2022:code' column to 'code' if it exists
if 'CEN2022:code' in geodata.columns:
    geodata.rename(columns={"CEN2022:code": "code"}, inplace=True)

# Handle duplicate rows based on the 'code' column
if geodata['code'].duplicated().any():
    print("Duplicate 'code' values detected in GeoDataFrame. Removing duplicates...")
    geodata = geodata.drop_duplicates(subset='code')

# Verify final GeoDataFrame structure
#print("GeoDataFrame after cleanup:")
#print(geodata.head())
#print(geodata.columns)

# CSV Processing
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(csv_folder, file)

        # Load CSV with error handling
        census_data = pd.read_csv(
            file_path,
            dtype={
                "code": str, #All codes treated as stringns
                "OBJECTID": int,
            },
            on_bad_lines='skip', header=0,
            low_memory=False
        )
        print(f"Processing file: {file}")
        print(f"Initial rows in {file}:")
        print(census_data.head())

        # Rename the first column to 'code'
        census_data.rename(columns={census_data.columns[0]: 'code'}, inplace=True)

        # Remove duplicate columns and rows
        census_data = census_data.loc[:, ~census_data.columns.duplicated()]
        if census_data['code'].duplicated().any():
            print(f"Duplicate 'code' values found in {file}. Removing duplicates...")
            census_data = census_data.drop_duplicates(subset='code')

        # Detect missing data, validate key columns in current file, and skip if critical info missing
        print(f"Missing data in {file}:")
        print(census_data.isnull().sum())
        if census_data[['code']].isnull().any().any():
            print(f"Critical missing data found in {file}. Skipping file.")
            continue  # Skip this file if critical data is missing
        geo_df = geo_df.merge(census_data, on="code", how="left")  # Perform the merge

        # Example: Filling or dropping missing data
        census_data = census_data.fillna(0)  # Replace all NaNs with 0

        # Merge data into GeoDataFrame
        print(f"Merging data from {file} with GeoDataFrame...")
        geodata = geodata.merge(census_data, how="left", on="code")

#Verify the final merged frame
print("Missing data in final merged GeoDataFrame:")
print(geo_df.isnull().sum())  # Check for missing values post-merge

#Handle remaining missing data in GeoDataFrame
# Option 1: Replace missing values
geo_df['Popcount'] = geo_df['Popcount'].fillna(0)  # Replace NaN with 0
geo_df['HHcount'] = geo_df['HHcount'].fillna(geo_df['HHcount'].mean())  # Fill with mean

#Validate geometry
geo_df['geometry'] = geo_df['geometry'].apply(make_valid) #Fixes invalid geometries
print("Invalid geometries after merging:", geo_df[~geo_df.is_valid])

# Verify final merged GeoDataFrame
print("Final GeoDataFrame after merging with CSVs:")
print(geodata.head())

# Save the result
output_file = "cleaned_geodata.gpkg"
geodata.to_file(output_file, driver="GPKG")
print(f"Cleaned and merged GeoDataFrame saved to {output_file}.")
