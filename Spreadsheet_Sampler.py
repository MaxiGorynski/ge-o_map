import pandas as pd

def Spreadsheet_Sampler(import_csv, output_csv):

    data = pd.read_csv(import_csv)

    first_ten_rows = data.head(10)

    first_ten_rows.to_csv(output_csv, index=False)

input_csv = 'westminster-parliamentary-constituencies.csv'
output_csv = 'westminster-constituencies-cropped.csv'

Spreadsheet_Sampler(input_csv, output_csv)
