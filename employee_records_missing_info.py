import pandas as pd

df = pd.read_excel("Employee View.xls", sheet_name="Sheet - 1")

pivot_table = df.pivot_table(
    values=['Permanent Residency Card', 'W4', 'Social Security', 'Birth Certificate', 'Passport', 'E verification', 'Physical Test', 'ID', 'Application', 'Work Authorization', 'Drug test', 'Resume'],
    index='Employee ID',
    aggfunc=lambda x: x.isnull().sum()
)

# Replace 1 values with 'Missing'
pivot_table = pivot_table.where(pivot_table != 1, 'Missing')

# Write the modified pivot table to an Excel file
pivot_table.to_excel("missing_documents_pivot.xlsx")

print("Pivot table saved to missing_documents_pivot.xlsx")
