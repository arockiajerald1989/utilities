import pandas as pd
import openpyxl

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

# Optionally, write the merged DataFrame to a new Excel file
df_merged.to_excel('TS.xlsx', index=False)

# Load data from Excel sheets
df1 = pd.read_excel("TS.xlsx")
df2 = pd.read_excel("Mapping.xlsx")

# Specify the required columns from each DataFrame
required_columns_df1 = ["FullName", "ID", "Project", "Team", "Hours"]  # Adjust as needed
required_columns_df2 = ["ID", "SS ID"]

# Extract only the required columns
df1 = df1[required_columns_df1]
df2 = df2[required_columns_df2]

# Merge DataFrames based on common columns
merged_df = df1.merge(df2, on="ID", how='left')  # Use 'inner' for intersection

# Rearrange columns to the desired order
merged_df = merged_df[["FullName", "SS ID", "ID", "Project", "Team", "Hours"]]

# Write the merged DataFrame to a new Excel sheet, including only extracted columns
merged_df.to_excel("merged_data.xlsx", index=False)
print("Excel sheets merged successfully!")

# Reopen the Excel file for formatting
workbook = openpyxl.load_workbook('merged_data.xlsx')
worksheet = workbook.active

# Autofit columns
for column in worksheet.columns:
    worksheet.column_dimensions[column[1].column_letter].auto_size = True
worksheet.column_dimensions['A'].width = 30

# Save the formatted workbook
workbook.save('merged_data.xlsx')
