import geopandas as gpd
import pandas as pd
import os

# Paths
csv_folder = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area"
gml_file = "CEN2022_OA.xml"

# Load GeoDataFrame
geodata = gpd.read_file(gml_file)

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
print("GeoDataFrame after cleanup:")
print(geodata.head())
print(geodata.columns)

# CSV Processing
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(csv_folder, file)

        # Load CSV with error handling
        census_data = pd.read_csv(file_path, on_bad_lines='skip', header=0)
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

        # Merge data into GeoDataFrame
        print(f"Merging data from {file} with GeoDataFrame...")
        geodata = geodata.merge(census_data, how="left", on="code")

# Verify final merged GeoDataFrame
print("Final GeoDataFrame after merging with CSVs:")
print(geodata.head())

# Save the result
output_file = "cleaned_geodata.gpkg"
geodata.to_file(output_file, driver="GPKG")
print(f"Cleaned and merged GeoDataFrame saved to {output_file}.")
