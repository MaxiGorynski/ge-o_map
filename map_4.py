import pandas as pd
import xml.etree.ElementTree as ET
import rasterio
from rasterio.plot import show
from pyproj import Proj, transform
import matplotlib.pyplot as plt

tif_file = "/Users/supriyarai/Code/ge-o_map/Over_gb/GBOverview.tif"
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area/UV101b - Usual resident population by sex by age (6).csv"
xml_file = "/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml"

#Load TIFF map file
with rasterio.open(tif_file) as src:
    tif_data = src.read(1)
    transform_tif = src.transform

#Read CSV file
csv_data = pd.read_csv(csv_file, delimiter=",", on_bad_lines="skip")
csv_data = csv_data[csv_data.iloc[:, 0].str.startswith("S001", na=False)]

#Parse XML
tree = ET.parse(xml_file)
root = tree.getroot()

namespace = {"CEN2022": "/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml"}

#Dictionary to store data
overlay_data = []

#Process each row in the CSV
for _, row in csv_data.iterrows():
    oa_code = row[0]
    data_values = row[1:]

    #Find matching OA in XML file
    xpath = f"/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml[CEN2022:code='{oa_code}']"
    oa_element = root.find(xpath, namespace)
    if oa_element is not None:
        easting = float(oa_element.find("CEN2022:easting", namespace).text)
        northing = float(oa_element.find("CEN2022:northing", namespace).text)

        #Convert BNG to WGS84
        bng_proj = Proj(init="epsg:27700")
        wgs84_proj = Proj(init="espg:4326")
        lon, lat = transform(bng_proj, wgs84_proj, easting, northing)

        overlay_data.append({
            "oa_code": oa_code,
            "lon": lon,
            "lat": lat,
            "values": data_values.tolist()
        })

#Plot TIFF map with overlay
plt.figure(figsize=(10, 10))
show(tif_data, transform=transform_tif, cmap="gray")

#Overlay points on map
for data in overlay_data:
    plt.scatter(data["lon"], data["lat"], label=data["oa_code"], s=10, c=red)

plt.legend()
plt.title("Census Data Overlay")
plt.show()