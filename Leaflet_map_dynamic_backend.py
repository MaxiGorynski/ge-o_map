import pandas as pd
import json
import os

#Dataframe for CSV
csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area-Full/UV101b - Usual resident population by sex by age (Full Geo).csv"
data = pd.read_csv(csv_file)

#Output folder
output_folder = "/Users/supriyarai/Code/ge-o_map/Map_JSON"

#Turn DF to dict list
data_list = data.to_dict(orient="records")

#Get name of csv file
csv_name = os.path.splitext(os.path.basename(csv_file))[0]

#Specify JSON filename and destination
json_file = os.path.join(output_folder, f"output.json.{csv_name}")
os.makedirs(output_folder, exist_ok=True)

#Save data to JSON file
with open (json_file, "w", encoding="utf-8") as f:
    json.dump(data_list, f, indent=4, ensure_ascii=False)

print(f"JSON saved to {json_file}")