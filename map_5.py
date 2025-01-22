import pandas as pd
import folium
import xml.etree.ElementTree as ET
from folium import plugins

#Filepaths
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-OA-Modded/Scotland Census 22 - UV102b - Age (20) by sex - UV102b - Age (20) by sex.csv"
gml_file = "/Users/supriyarai/Code/ge-o_map/bdline_gml3_gb/Data/INSPIRE_AdministrativeUnit.gml"

# Load the CSV data
data = pd.read_csv(csv_file)
oa_code = data['OA_Code']
latitude = data['Latitude']
longitude = data['Longitude']
all_people = data['All people']
female_all = data['Female, All']
male_all = data['Male, All']

#Parse GML
tree = ET.parse(gml_file)
root = tree.getroot()

#Extract position list data (i.e. coordinates for the constituency boundaries)
positions = []
for posList in root.findall(".//gml:posList", namespaces={'gml': 'http://www.opengis.net/gml'}):
    coordinates = posList.text.strip().split()
    positions.append([(float(coordinates[i]), float(coordinates[i + 1])) for i in range(0, len(coordinates), 2)])

#Create folium map
uk_map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)

#Add boundary polygons (red)
for boundary in positions:
    folium.Polygon(
        locations=boundary,
        color='red',
        weight=2,
        fill=False
    ).add_to(uk_map)

#Feature groups for datasets
all_people_group = folium.FeatureGroup(name="Number of People", show=True)
female_group = folium.FeatureGroup(name="Female, All", show=True)
male_group = folium.FeatureGroup(name="Male, All", show=True)

#Dots with popups for datasets
for oa, lat, lon, people, female, male in zip(oa_code, latitude, longitude, all_people, female_all, male_all):
    if not pd.isnull(lat) and not pd.isnull(lon):
        #Add marker for "Number of People"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Number of People: {people}", max_width=300)
        ).add_to(all_people_group)

        #Add marker for "Female, All"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='purple',
            fill=True,
            fill_color='purple',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Female, All: {female}", max_width=300)
        ).add_to(female_group)

        #Add marker for "Male, All"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Male, All: {male}", max_width=300)
        ).add_to(male_group)

#Add feature groups to map
all_people_group.add_to(uk_map)
female_group.add_to(uk_map)
male_group.add_to(uk_map)

#Add layer control to toggle visibility of the groups
folium.LayerControl(position='topright', collapsed=False).add_to(uk_map)

#Save map to HTML file
map_file = "uk_with_boundaries_and_gender_dots.html"
uk_map.save(map_file)

print(f"Map saved to {map_file}")
