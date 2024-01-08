import pandas as pd

# Specify the filename and sheet name
filename = 'TS.xls'  # Replace with your actual filename
sheet_name = 'Details'  # Replace if your data is in a different sheet

# Read the Excel file into a DataFrame, stopping at the first empty row
df = pd.read_excel(filename, sheet_name=sheet_name, header=0, nrows=None)

empty_row_index = df.index[df.isnull().all(axis=1)].tolist()[0]

# Select rows up to (but not including) the empty row
df = df.iloc[:empty_row_index]

# Group the DataFrame by ID and FullName, summing the Hours
df_merged = df.groupby(['ID', 'FullName'])['Hours'].sum().reset_index()

# Optionally, write the merged DataFrame to a new Excel file
df_merged.to_excel('merged_output.xlsx', index=False)
