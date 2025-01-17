from shapely.geometry import Polygon, box
import geopandas as gpd
from lxml import etree
import matplotlib.pyplot as plt


def parse_xml(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()

    namespaces = {
        'gml': 'http://www.opengis.net/gml',
        'CEN2022': 'maps.gov.scot'
    }

    data = []
    invalid_features = 0

    for feature in root.xpath('//gml:featureMember', namespaces=namespaces):
        code = feature.xpath('.//CEN2022:code/text()', namespaces=namespaces)[0]
        popcount = feature.xpath('.//CEN2022:Popcount/text()', namespaces=namespaces)[0]
        hhcount = feature.xpath('.//CEN2022:HHcount/text()', namespaces=namespaces)[0]

        pos_list = feature.xpath('.//gml:posList/text()', namespaces=namespaces)

        if pos_list:
            coords = []
            coord_pairs = pos_list[0].split()
            for i in range(0, len(coord_pairs), 2):
                try:
                    lon = float(coord_pairs[i])
                    lat = float(coord_pairs[i + 1])
                    coords.append((lon, lat))
                except (ValueError, IndexError):
                    print(f"Invalid coordinate pair skipped: {coord_pairs[i:i + 2]}")

            if pos_list:
                coords = []
                coord_pairs = pos_list[0].split()  # Access the first element of pos_list
                for i in range(0, len(coord_pairs), 2):
                    try:
                        lon = float(coord_pairs[i])
                        lat = float(coord_pairs[i + 1])
                        coords.append((lon, lat))
                    except (ValueError, IndexError):
                        print(f"Invalid coordinate pair skipped: {coord_pairs[i:i + 2]}")

                print(f"Raw coordinates for {code}: {coords[:10]}...")  # Debug: First 10 coords

                if len(coords) >= 3:  # Ensure valid polygon
                    polygon = Polygon(coords)
                    if polygon.is_valid:
                        data.append({
                            'code': code,
                            'popcount': int(popcount),
                            'hhcount': int(hhcount),
                            'geometry': polygon
                        })
                    else:
                        print(f"Invalid polygon for {code}. Skipping...")
                        invalid_features += 1
                else:
                    print(f"Too few points to form a polygon for {code}. Skipping...")
                    invalid_features += 1
            else:
                print(f"No posList found for {code}. Skipping...")
                invalid_features += 1

    geo_df = gpd.GeoDataFrame(data, crs='EPSG:27700')
    print(f"GeoDataFrame bounds: {geo_df.total_bounds}")  # Insert here
    print(f"Skipped {invalid_features} invalid features.")

    # Debug original CRS and reproject
    if geo_df.crs is None:
        geo_df.set_crs('EPSG:4326', allow_override=True, inplace=True)
    geo_df = geo_df.to_crs('EPSG:27700')
    print(f"Reprojected CRS: {geo_df.crs}")

    # Fix invalid geometries if needed
    geo_df['geometry'] = geo_df['geometry'].buffer(0)

    if not geo_df.empty:
        print(f"Initial CRS: {geo_df.crs}")  # Debug: Check initial CRS
        geo_df.set_crs('EPSG:27700', allow_override=True, inplace=True)
        geo_df = geo_df.to_crs('EPSG:27700')  # Reproject data
    else:
        print("Error: No valid geometries found in the XML.")

    return geo_df


xml_file = "/Users/supriyarai/Code/ge-o_map/CEN2022_OA.xml"
geo_df = parse_xml(xml_file)

if not geo_df.empty:
    print(f"Final CRS: {geo_df.crs}")  # Debug: Check final CRS
    print(f"GeoDataFrame bounds: {geo_df.total_bounds}")  # Check spatial extent
    print(geo_df.head())  # Debug: Preview first rows

    # Visualize
    geo_df.plot(column='popcount', cmap='Oranges', legend=True, figsize=(10, 10))
    #Overlay with Scotland shapefile
    scotland = gpd.read_file('/path/to/scotland_shapefile.shp')
    scotland = scotland.to_crs('EPSG:27700')

    ax = scotland.plot(color='lightblue', edgecolor='black', figsize=(10, 10))
    geo_df.plot(ax=ax, column='popcount', cmap='Oranges', legend=True, alpha=0.7)
    plt.title('Your Data Overlaid on Scotland Map')
    plt.show()

    plt.title('Population Count by Area')
    plt.show()
else:
    print("GeoDataFrame is empty. No map to display.")
