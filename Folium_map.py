import pandas as pd
import folium
import xml.etree.ElementTree as ET
from folium import plugins
from folium.plugins import FeatureGroupSubGroup

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
all_people_0_4 = data['All people, 0 - 4']
all_people_5_9 = data['All people, 5 - 9']
all_people_10_14 = data['All people, 10 - 14']
all_people_15 = data['All people, 15']
all_people_16_17 = data['All people, 16 - 17']
all_people_18_19 = data['All people, 18 - 19']
all_people_20_24 = data['All people, 20 - 24']
all_people_25_29 = data['All people, 25 - 29']
all_people_30_34 = data['All people, 30 - 34']
all_people_35_39 = data['All people, 35 - 39']
all_people_40_44 = data['All people, 40 - 44']
all_people_45_49 = data['All people, 45 - 49']
all_people_50_54 = data['All people, 50 - 54']
all_people_55_59 = data['All people, 55 - 59']
all_people_60_64 = data['All people, 60 - 64']
all_people_65_69 = data['All people, 65 - 69']
all_people_70_74 = data['All people, 70 - 74']
all_people_75_79 = data['All people, 75 - 79']
all_people_80_84 = data['All people, 80 - 84']
all_people_85_over = data['All people, 85 and over']

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

#Parent groups for drop-down menus
all_people_parent_group = folium.FeatureGroup(name="All People", show=False)

#Add parent group to map
all_people_parent_group.add_to(uk_map)

#Feature groups for datasets
female_group = folium.FeatureGroup(name="Female, All", show=False)
male_group = folium.FeatureGroup(name="Male, All", show=False)
all_people_group = FeatureGroupSubGroup(all_people_parent_group, "Total Number of People", show=False)
all_people_0_4_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 0-4", show=False)
all_people_5_9_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 5-9", show=False)
all_people_10_14_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 10-14", show=False)
all_people_15_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 15", show=False)
all_people_16_17_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 16-17", show=False)
all_people_18_19_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 18-19", show=False)
all_people_20_24_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 20-24", show=False)
all_people_25_29_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 25-29", show=False)
all_people_30_34_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 30-34", show=False)
all_people_35_39_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 35-39", show=False)
all_people_40_44_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 40-44", show=False)
all_people_45_49_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 45-49", show=False)
all_people_50_54_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 50-54", show=False)
all_people_55_59_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 55-59", show=False)
all_people_60_64_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 60-64", show=False)
all_people_65_69_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 65-69", show=False)
all_people_70_74_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 70-74", show=False)
all_people_75_79_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 75-79", show=False)
all_people_80_84_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 80-84", show=False)
all_people_85_and_over_group = FeatureGroupSubGroup(all_people_parent_group, "All People, 85 and over", show=False)


#Dots with popups for datasets
for oa, lat, lon, people, female, male, all_people_0_4, all_people_5_9, all_people_10_14, all_people_15, all_people_16_17, all_people_18_19, all_people_20_24, all_people_25_29, all_people_30_34, all_people_35_39, all_people_40_44, all_people_45_49, all_people_50_54, all_people_55_59, all_people_60_64, all_people_65_69, all_people_70_74, all_people_75_79, all_people_80_84, all_people_85_over in zip(oa_code, latitude, longitude, all_people, female_all, male_all, all_people_0_4, all_people_5_9, all_people_10_14, all_people_15, all_people_16_17, all_people_18_19, all_people_20_24, all_people_25_29, all_people_30_34, all_people_35_39, all_people_40_44, all_people_45_49, all_people_50_54, all_people_55_59, all_people_60_64, all_people_65_69, all_people_70_74, all_people_75_79, all_people_80_84, all_people_85_over):
    if not pd.isnull(lat) and not pd.isnull(lon):
        # Add marker for "Number of People"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Number of People: {people}", max_width=300)
        ).add_to(all_people_group)

        #Marker for "All people" categories
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
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 10-14: {all_people_10_14}", max_width=300)
        ).add_to(all_people_10_14_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 15: {all_people_15}", max_width=300)
        ).add_to(all_people_15_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 16-17: {all_people_16_17}", max_width=300)
        ).add_to(all_people_16_17_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 18-19: {all_people_18_19}", max_width=300)
        ).add_to(all_people_18_19_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People,aged 20-24: {all_people_20_24}", max_width=300)
        ).add_to(all_people_20_24_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 25-29: {all_people_25_29}", max_width=300)
        ).add_to(all_people_25_29_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 30-34: {all_people_30_34}", max_width=300)
        ).add_to(all_people_30_34_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 35-39: {all_people_35_39}", max_width=300)
        ).add_to(all_people_35_39_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 40-44: {all_people_40_44}", max_width=300)
        ).add_to(all_people_40_44_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 45-49: {all_people_45_49}", max_width=300)
        ).add_to(all_people_45_49_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 50-54: {all_people_50_54}", max_width=300)
        ).add_to(all_people_50_54_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 55-59: {all_people_55_59}", max_width=300)
        ).add_to(all_people_55_59_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 60-64: {all_people_60_64}", max_width=300)
        ).add_to(all_people_60_64_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 65-69: {all_people_65_69}", max_width=300)
        ).add_to(all_people_65_69_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 70-74: {all_people_70_74}", max_width=300)
        ).add_to(all_people_70_74_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 75-79: {all_people_75_79}", max_width=300)
        ).add_to(all_people_75_79_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 80-84: {all_people_80_84}", max_width=300)
        ).add_to(all_people_80_84_group)

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='cyan',
            fill=True,
            fill_color='cyan',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All People, aged 85 and above: {all_people_85_over}", max_width=300)
        ).add_to(all_people_85_and_over_group)

        # Add marker for "Female, All"
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='purple',
            fill=True,
            fill_color='purple',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>Female, All: {female}", max_width=300)
        ).add_to(female_group)

        # Add marker for "Male, All"
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
all_people_0_4_group.add_to(uk_map)
all_people_5_9_group.add_to(uk_map)
all_people_10_14_group.add_to(uk_map)
all_people_15_group.add_to(uk_map)
all_people_16_17_group.add_to(uk_map)
all_people_18_19_group.add_to(uk_map)
all_people_20_24_group.add_to(uk_map)
all_people_25_29_group.add_to(uk_map)
all_people_30_34_group.add_to(uk_map)
all_people_35_39_group.add_to(uk_map)
all_people_40_44_group.add_to(uk_map)
all_people_45_49_group.add_to(uk_map)
all_people_50_54_group.add_to(uk_map)
all_people_55_59_group.add_to(uk_map)
all_people_60_64_group.add_to(uk_map)
all_people_65_69_group.add_to(uk_map)
all_people_70_74_group.add_to(uk_map)
all_people_75_79_group.add_to(uk_map)
all_people_80_84_group.add_to(uk_map)
all_people_85_and_over_group.add_to(uk_map)

#Add layer control to toggle visibility of the groups
folium.LayerControl(position='topright', collapsed=False).add_to(uk_map)

#Save map to HTML file
map_file = "uk_with_boundaries_and_gender_dots.html"
uk_map.save(map_file)

print(f"Map saved to {map_file}")
