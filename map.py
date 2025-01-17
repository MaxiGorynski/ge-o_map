import geopandas as gpd
import matplotlib.pyplot as plt
from lxml import etree
from shapely.geometry import Polygon


# Function to parse XML and extract polygons
def parse_xml(xml_file):
    # Parse the XML file
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # Namespace mapping for easier parsing
    namespaces = {
        'gml': 'http://www.opengis.net/gml',
        'CEN2022': 'maps.gov.scot'
    }

    # List to hold data
    data = []

    # Iterate through each feature in the XML
    for feature in root.xpath('//gml:featureMember', namespaces=namespaces):
        # Extract relevant fields
        code = feature.xpath('.//CEN2022:code/text()', namespaces=namespaces)[0]
        popcount = feature.xpath('.//CEN2022:Popcount/text()', namespaces=namespaces)[0]
        hhcount = feature.xpath('.//CEN2022:HHcount/text()', namespaces=namespaces)[0]

        # Extract geometry
        pos_list = feature.xpath('.//gml:posList/text()', namespaces=namespaces)

        # Check if pos_list is not empty and contains valid data
        if pos_list:
            coords = []
            # Split the posList string into individual coordinates
            coord_pairs = pos_list[0].split()
            for i in range(0, len(coord_pairs), 2):  # Process pairs of coordinates (lon, lat)
                try:
                    lon = float(coord_pairs[i])  # Longitude
                    lat = float(coord_pairs[i + 1])  # Latitude
                    coords.append((lon, lat))
                except ValueError:
                    print(f"Invalid coordinate pair: {coord_pairs[i]}, {coord_pairs[i + 1]}. Skipping...")

            # Create a Polygon from the coordinates if there are valid ones
            if coords:
                polygon = Polygon(coords)
                # Append data
                data.append({
                    'code': code,
                    'popcount': popcount,
                    'hhcount': hhcount,
                    'geometry': polygon
                })
        else:
            print(f"No valid posList found for code {code}. Skipping...")

    # Convert to GeoDataFrame
    geo_df = gpd.GeoDataFrame(data)

    # Check if data contains valid geometries
    if not geo_df.empty and geo_df.geometry.isna().sum() == 0:
        # Set the CRS to EPSG:27700 (British National Grid)
        geo_df.set_crs('EPSG:27700', allow_override=True, inplace=True)
    else:
        print("Error: No valid geometries found.")

    # Return GeoDataFrame
    return geo_df


# Path to your XML file
xml_file = "/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml"

# Parse the XML and convert it to GeoDataFrame
geo_df = parse_xml(xml_file)

# If the GeoDataFrame is not empty, plot the data
if not geo_df.empty:
    geo_df.set_geometry('geometry', inplace=True)  # Explicitly set the geometry column
    geo_df.plot(column='popcount', cmap='Oranges', legend=True)
    plt.title('Population Count by Area')
    plt.show()
else:
    print("GeoDataFrame is empty or contains no valid data.")
