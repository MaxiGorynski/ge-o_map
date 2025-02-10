import xml.etree.ElementTree as ET
import json

# File path placeholder
GML_FILE_PATH = "/Users/supriyarai/Code/ge-o_map/bdline_gml3_gb/Data/INSPIRE_AdministrativeUnit.gml"
OUTPUT_JSON_PATH = "static/epsg27700_boundaries.json"

def extract_epsg27700_coordinates(gml_file):
    print("🔄 Extracting EPSG:27700 coordinates from GML file...")

    # Parse the GML file
    tree = ET.parse(gml_file)
    root = tree.getroot()

    # Define namespace mappings (modify as needed)
    namespaces = {
        "gml": "http://www.opengis.net/gml/3.2",
        "au": "http://inspire.ec.europa.eu/schemas/au/4.0",
    }

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Find all administrative units (boundaries)
    units = root.findall(".//au:AdministrativeUnit", namespaces)
    total_units = len(units)

    if total_units == 0:
        print("❌ No administrative units found! Check your GML structure.")
        return None

    print(f"📌 Found {total_units} administrative boundaries. Extracting...")

    for idx, unit in enumerate(units, start=1):
        unit_id = unit.get("{http://www.opengis.net/gml/3.2}id")

        pos_list_element = unit.find(".//gml:posList", namespaces)
        if pos_list_element is not None:
            pos_list_text = pos_list_element.text.strip()
            epsg27700_coords = list(map(float, pos_list_text.split()))

            # Format into GeoJSON structure (no conversion)
            lat_lon_coords = [[epsg27700_coords[i], epsg27700_coords[i + 1]] for i in range(0, len(epsg27700_coords), 2)]

            feature = {
                "type": "Feature",
                "properties": {"unit_id": unit_id},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [lat_lon_coords]  # Keep as EPSG:27700
                }
            }
            geojson_data["features"].append(feature)

        # Progress logging every 100 entries
        if idx % 100 == 0:
            print(f"✅ Processed {idx}/{total_units} boundaries.")

    print(f"✅ Extraction complete! Saving to {OUTPUT_JSON_PATH}")

    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(geojson_data, f, indent=4)

    print(f"🎉 GeoJSON saved as {OUTPUT_JSON_PATH}")

# Run extraction
extract_epsg27700_coordinates(GML_FILE_PATH)
