import pandas as pd

# Specify filenames and sheet names
filename1 = 'V1.xlsx'  # Replace with the actual filename for V1
sheet_name1 = 'Details'  # Replace with the actual sheet name for V1 if different
filename2 = 'V2.xlsx'  # Replace with the actual filename for V2
sheet_name2 = 'Details'  # Replace with the actual sheet name for V2 if different

# Read the Excel files, stopping at the first empty row in each
df1 = pd.read_excel(filename1, sheet_name=sheet_name1, header=0, nrows=None)
df2 = pd.read_excel(filename2, sheet_name=sheet_name2, header=0, nrows=None)

# Identify empty row indices
empty_row_index1 = df1.index[df1.isnull().all(axis=1)].tolist()[0]
empty_row_index2 = df2.index[df2.isnull().all(axis=1)].tolist()[0]

# Select rows up to (but not including) the empty rows
df1 = df1.iloc[:empty_row_index1]
df2 = df2.iloc[:empty_row_index2]

# Total the Hours by FullName and ID for each file separately, ensuring MultiIndex
total_hours_v1 = df1.groupby(['FullName', 'ID'])['Hours'].sum().reset_index()  # Reset index to create MultiIndex
total_hours_v2 = df2.groupby(['FullName', 'ID'])['Hours'].sum().reset_index()

# Optionally, write the results to separate Excel sheets
total_hours_v1.to_excel('total_hours_v1.xlsx')
total_hours_v2.to_excel('total_hours_v2.xlsx')

# Merge the total_hours DataFrames
df_merged = pd.merge(total_hours_v1, total_hours_v2, on=['FullName', 'ID'], suffixes=('_V1', '_V2'))

# Add the Difference Hours column
df_merged['Difference Hours'] = df_merged['Hours_V2'] - df_merged['Hours_V1']

# Rearrange columns in the desired order
df_merged = df_merged[['ID', 'FullName', 'Hours_V1', 'Hours_V2', 'Difference Hours']]

# Write the merged DataFrame to a new Excel sheet
df_merged.to_excel('merged_output.xlsx', index=False)
