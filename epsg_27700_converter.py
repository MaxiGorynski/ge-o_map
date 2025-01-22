import pandas as pd
from pyproj import Transformer

# File path
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-OA-Modded/UV102b - Age (20) by sex - Basic.csv"

# Initialize the transformer for EPSG:4326 (WGS84) -> EPSG:27700 (British National Grid)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Check if columns for Latitude and Longitude exist (adjust column names as per the actual file)
lat_col = "Latitude"  # Replace with the actual column name for Latitude in your CSV
lon_col = "Longitude"  # Replace with the actual column name for Longitude in your CSV

if lat_col not in df.columns or lon_col not in df.columns:
    raise ValueError(f"Columns '{lat_col}' and '{lon_col}' must exist in the CSV file.")

# Perform the coordinate transformation
def convert_to_epsg27700(lat, lon):
    """Convert Latitude and Longitude to EPSG:27700 coordinates."""
    if pd.notna(lat) and pd.notna(lon):  # Only process non-null values
        easting, northing = transformer.transform(lon, lat)  # Note: Transformer expects lon, lat order
        return easting, northing
    return None, None

# Apply the transformation and create new columns
df[['Easting', 'Northing']] = df.apply(
    lambda row: pd.Series(convert_to_epsg27700(row[lat_col], row[lon_col])),
    axis=1
)

# Save the updated DataFrame back to the CSV file
output_file = csv_file.replace(".csv", "_with_EPSG27700.csv")
df.to_csv(output_file, index=False)

print(f"Updated file with EPSG:27700 coordinates saved to: {output_file}")
