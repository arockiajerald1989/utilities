import pandas as pd

# Load the Excel file
df = pd.read_excel('output_file.xlsx')
column_length = len(df.columns)
print("column_length :", column_length)

# Extract names and numbers using regular expressions
df[['Name', 'Number']] = df['name'].str.extract(r"(.*) \((\d+)\)")

df = df.drop('name', axis=1)

column_length = len(df.columns)
print("column_length :", column_length)

# Extract regular and overtime hours
overtime_threshold = 40
df['Regular Hours'] = df['Total Hours'].clip(upper=overtime_threshold)
df['Overtime Hours'] = df['Total Hours'] - df['Regular Hours']

df = df[['Name', 'Number'] + list(df.columns[0:column_length-3]) + ['Total Hours', 'Regular Hours', 'Overtime Hours']]

# Write the results to a new Excel file with auto-fitted columns
with pd.ExcelWriter('extracted_data.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
    workbook = writer.book  # Access the workbook
    worksheet = workbook.active  # Access the active worksheet
    for column in worksheet.columns:
        worksheet.column_dimensions[column[0].column_letter].auto_size = True
