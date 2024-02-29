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
df_merged = df.groupby(['ID', 'FullName', 'Project', 'Team'])['Hours'].sum().reset_index()

# Sort the DataFrame by FullName before saving
df_merged = df_merged.sort_values(by=['FullName'], ascending=True)

# Extract regular and overtime hours
overtime_threshold = 40
df_merged['Regular Hours'] = df_merged['Hours'].clip(upper=overtime_threshold)
df_merged['Overtime Hours'] = df_merged['Hours'] - df_merged['Regular Hours']

df_merged = df_merged[['FullName', 'ID'] + ['Hours', 'Regular Hours', 'Overtime Hours']]

# Optionally, write the merged DataFrame to a new Excel file
df_merged.to_excel('TS.xlsx', index=False)
