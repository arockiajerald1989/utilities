import pandas as pd
import openpyxl

# Specify the filename and sheet name
filename = 'TS.xls'  # Replace with your actual filename
sheet_name = 'Detail'  # Replace if your data is in a different sheet

# Read the Excel file into a DataFrame, stopping at the first empty row
df = pd.read_excel(filename, sheet_name=sheet_name, header=0, nrows=None)

empty_row_index = df.index[df.isnull().all(axis=1)].tolist()[0]

# Select rows up to (but not including) the empty row
df = df.iloc[:empty_row_index]

pivot_table = df.pivot_table(
    values='Hours',  # Assuming the column to aggregate is 'Hours'
    index=['Project', 'Team', 'WorkersType'],
    columns='PayRule',
    aggfunc='sum',
    fill_value=0
)

writer = pd.ExcelWriter("invoice.xlsx")  # Replace with the desired output file path

# Sequence the column headers
pivot_table = pivot_table[['Regular', 'Overtime']]  # Rearrange columns as needed
pivot_table.to_excel(writer, sheet_name="Pivot Table")
writer._save()

# Reopen the Excel file for formatting
workbook = openpyxl.load_workbook('invoice.xlsx')
worksheet = workbook.active

# Autofit columns
for column in worksheet.columns:
    worksheet.column_dimensions[column[1].column_letter].auto_size = True
worksheet.column_dimensions['C'].width = 25

# Save the formatted workbook
workbook.save('invoice.xlsx')
