import csv
import xml.etree.ElementTree as ET
from pyproj import Proj, transform

# File paths
xml_file = "/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml"
output_csv = "output_coordinates.csv"

# Define projections for coordinate conversion
bng_proj = Proj(init="epsg:27700")  # British National Grid
wgs84_proj = Proj(init="epsg:4326")  # WGS84 (latitude/longitude)

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Define the namespace (update if necessary)
namespace = {"CEN2022": "maps.gov.scot"}  # Replace this with your XML namespace

# Write data to the CSV file
with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["OA_Code", "Latitude", "Longitude"])  # Write header

    # Iterate through each OutputArea2022 element in the XML file
    for output_area in root.findall(".//CEN2022:OutputArea2022", namespace):
        # Extract the OA code, easting, and northing
        oa_code = output_area.find("CEN2022:code", namespace).text
        easting = float(output_area.find("CEN2022:easting", namespace).text)
        northing = float(output_area.find("CEN2022:northing", namespace).text)

        # Convert easting/northing to latitude/longitude
        lon, lat = transform(bng_proj, wgs84_proj, easting, northing)

        # Write the extracted and converted data to the CSV
        writer.writerow([oa_code, lat, lon])

print(f"Data has been successfully written to {output_csv}.")
