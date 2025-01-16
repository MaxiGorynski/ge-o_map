
add_code_column_label(csv_folder)

if geodata['code'].duplicated().any():
    print("Duplicate 'code' values in GeoDataFrame")
    geodata = geodata.drop_duplicates(subset='code')

for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(csv_folder, file)
        # Load CSV with additional error handling
        census_data = pd.read_csv(file_path, on_bad_lines='skip')  # Skip bad lines
        if census_data['code'].duplicated().any():
            print(f"Duplicate 'code' values in {file}")
            census_data = census_data.drop_duplicates(subset='code')
        if "code" in census_data.columns:
            geodata = geodata.merge(census_data, how="left", on="code")
        else:
            print(f"'code' column is missing in {file}")
            continue

#Verify final merged frame
print(geodata.head())