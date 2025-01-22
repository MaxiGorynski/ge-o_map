import pandas as pd
import folium

# Load the CSV file
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-OA-Modded/UV102b - Age (20) by sex - Basic_with_EPSG27700.csv"
data = pd.read_csv(csv_file)

# Extract the required columns
oa_code = data['OA_Code']
latitude = data['Latitude']
longitude = data['Longitude']
all_people = data['All people']

# Create a folium map centered on the UK
uk_map = folium.Map(location=[55.3781, -3.4360], zoom_start=6)

# Add individual dots with popups for each data point
for oa, lat, lon, people in zip(oa_code, latitude, longitude, all_people):
    if not pd.isnull(lat) and not pd.isnull(lon):
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,  # Size of the dot
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7,
            popup=folium.Popup(f"OA_Code: {oa}<br>All people: {people}", max_width=300)
        ).add_to(uk_map)

# Save the map to an HTML file
map_file = "uk_heatmap.html"
uk_map.save(map_file)

print(f"Heatmap saved to {map_file}")