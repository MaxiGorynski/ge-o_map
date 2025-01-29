import pandas as pd
import json

# Filepath
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area-Full/UV102b - Age (20) by sex.csv"

# Load the CSV data
data = pd.read_csv(csv_file)

# Prepare the data as a list of dictionaries
data_list = []
for _, row in data.iterrows():
    if not pd.isnull(row['Latitude']) and not pd.isnull(row['Longitude']):
        data_list.append({
            "oa_code": row['OA_Code'],
            "latitude": row['Latitude'],
            "longitude": row['Longitude'],
            "all_people": row['All people'],
            "male_all": row['Male, All'],
            "all_people_0_4": row['All people, 0 - 4'],
            "all_people_5_9": row['All people, 5 - 9']
        })

# Save data to a JSON file
output_file = "map_data.json"
with open(output_file, "w") as f:
    json.dump(data_list, f)

print(f"Data saved to {output_file}")
