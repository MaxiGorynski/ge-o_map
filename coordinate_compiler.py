import csv
import xml.etree.ElementTree as ET
import requests
from pyproj import Proj, transform

# Output CSV file path
output_csv = "final_output_coordinates.csv"

# Define projections for coordinate conversion
bng_proj = Proj(init="epsg:27700")  # British National Grid
wgs84_proj = Proj(init="epsg:4326")  # WGS84 (latitude/longitude)

# Base URL for WFS request
base_url = "https://maps.gov.scot/server/services/NRS/Census2022/MapServer/WFSServer"

# Query parameters
params = {
    "request": "GetFeature",
    "service": "WFS",
    "version": "1.1.0",
    "outputFormat": "text/xml; subtype=gml/3.1.1",
    "typeName": "CEN2022:OutputArea2022",
    "startIndex": 0,
    "maxFeatures": 1000,
}

# Namespace for parsing XML
namespace = {"CEN2022": "maps.gov.scot"}  # Replace if necessary

# Target OA code to stop at
stop_code = "S00181669"

# Open CSV file for writing
with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["OA_Code", "Latitude", "Longitude"])  # Write header

    while True:
        print(f"Fetching data from startIndex {params['startIndex']}...")
        response = requests.get(base_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break

        # Parse the XML response
        root = ET.fromstring(response.content)

        # Get OutputArea2022 elements
        output_areas = root.findall(".//CEN2022:OutputArea2022", namespace)
        if not output_areas:
            print("No more data found.")
            break

        for output_area in output_areas:
            # Extract OA code, easting, and northing
            oa_code = output_area.find("CEN2022:code", namespace).text
            easting = float(output_area.find("CEN2022:easting", namespace).text)
            northing = float(output_area.find("CEN2022:northing", namespace).text)

            # Convert coordinates
            lon, lat = transform(bng_proj, wgs84_proj, easting, northing)

            # Write to CSV
            writer.writerow([oa_code, lat, lon])

            # Stop processing if target OA code is found
            if oa_code == stop_code:
                print(f"Reached target OA code {stop_code}. Stopping.")
                exit(0)

        # Increment startIndex for next batch
        params["startIndex"] += params["maxFeatures"]

print(f"Data has been successfully written to {output_csv}.")
