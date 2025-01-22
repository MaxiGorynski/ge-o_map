import pandas as pd
import folium
from folium.plugins import FeatureGroupSubGroup

# Filepaths
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-OA-Modded/Scotland Census 22 - UV102b - Age (20) by sex - UV102b - Age (20) by sex.csv"

# Load the CSV data
data = pd.read_csv(csv_file)
oa_code = data['OA_Code']
latitude = data['Latitude']
longitude = data['Longitude']
all_people = data['All people']
male_all = data['Male, All']
all_people_0_4 = data['All people, 0 - 4']
all_people_5_9 = data['All people, 5 - 9']

# Create the map
uk_map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)

# Feature groups for datasets
all_people_group = folium.FeatureGroup(name="Number of People", show=True)
male_group = folium.FeatureGroup(name="Male, All", show=False)
all_people_0_4_group = folium.FeatureGroup(name="All People, 0-4", show=False)
all_people_5_9_group = folium.FeatureGroup(name="All People, 5-9", show=False)

# Add markers to each group
for oa, lat, lon, people, male, all_people_0_4, all_people_5_9 in zip(oa_code, latitude, longitude, all_people, male_all, all_people_0_4, all_people_5_9):
    if not pd.isnull(lat) and not pd.isnull(lon):
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Number of People: {people}", max_width=300)
        ).add_to(all_people_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 0-4: {all_people_0_4}", max_width=300)
        ).add_to(all_people_0_4_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 5-9: {all_people_5_9}", max_width=300)
        ).add_to(all_people_5_9_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Male, All: {male}", max_width=300)
        ).add_to(male_group)

# Add feature groups to the map
all_people_group.add_to(uk_map)
all_people_0_4_group.add_to(uk_map)
all_people_5_9_group.add_to(uk_map)
male_group.add_to(uk_map)

# Add layer control to toggle visibility of the groups
folium.LayerControl(position='topright', collapsed=False).add_to(uk_map)

# Save the map to HTML
map_file = "uk_with_boundaries_and_gender_dots.html"
uk_map.save(map_file)

print(f"Map saved to {map_file}")
