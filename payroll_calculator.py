import pandas as pd
import numpy as np

# Read the Excel files
df1 = pd.read_csv("final_report.csv")
# df2 = pd.read_excel("Rates.xlsx")
df2 = pd.read_excel("Rates.xlsx")

# Extract required columns
df1 = df1[["SS ID", "Total Hours", "Regular Hours", "Overtime Hours", "PerDiem/", "NightShift Allowance"]]
df2 = df2[["SS ID", "Pay rate 1", "Pay rate 2"]]

# Merge DataFrames
merged_df = df1.merge(df2, on='SS ID', how='left')

# Calculate total pay with conditional handling of null values and per diem
merged_df["Regular Earnings"] = (
    merged_df["Pay rate 1"] * merged_df["Regular Hours"]
)

merged_df["Overtime Earnings"] = (
    merged_df["Pay rate 1"] * merged_df["Overtime Hours"] * 1.5
)

merged_df["PerDiem Earnings"] = (
    merged_df["Pay rate 2"] * merged_df["PerDiem/"].astype(float)
)

merged_df["Total Earnings"] = (
    merged_df["Pay rate 1"] * merged_df["Regular Hours"]
    + np.where(pd.notnull(merged_df["Overtime Hours"]),
               merged_df["Overtime Hours"] * merged_df["Pay rate 1"] * 1.5,
               0)
    + np.where(pd.notnull(merged_df["PerDiem/"]),
               merged_df["Pay rate 2"] * merged_df["PerDiem/"].astype(float),
               0)
    + np.where(pd.notnull(merged_df["NightShift Allowance"]),
               merged_df["NightShift Allowance"] * 1.0,  # Assuming same pay rate for night shift
               0)
)

merged_df.to_excel("calculator_report.xlsx", index=False)

print("\n\nPayroll Summary")
print("-" * 15)  # Add a separator line

total_employees = merged_df["SS ID"].nunique()
print(f"Total Individuals Paid: {total_employees}")

total_hours = merged_df["Total Hours"].sum() + merged_df["PerDiem/"].astype(float).sum()
print(f"\nTotal Hours: {total_hours}")

total_overtime_hours = merged_df["Overtime Hours"].sum()
print(f"  Overtime Hours: {total_overtime_hours}")

total_perdiem_hours = merged_df["PerDiem/"].astype(float).sum()
print(f"  PerDiem Per Day Hours: {total_perdiem_hours}")
total_regular_hours = merged_df["Regular Hours"].sum()
print(f"  Regular Hours: {total_regular_hours}")

total_pay = merged_df["Total Earnings"].sum()
print(f"\nTotal Amounts: ${total_pay:,.2f}")  # Format currency with commas and 2 decimal places
total_nightshift_hours = merged_df["NightShift Allowance"].sum()
print(f"  NightShift Allowance Earnings: {total_nightshift_hours:,.2f}")

total_overtime_earnings = merged_df["Overtime Earnings"].sum()
print(f"  Overtime Earnings: ${total_overtime_earnings:,.2f}")

per_diem_earnings = merged_df["PerDiem Earnings"].sum()
print(f"  Per Diem Per Day Earnings: ${per_diem_earnings:,.2f}")

total_regular_earnings = merged_df["Regular Earnings"].sum()
print(f"  Regular Earnings: ${total_regular_earnings:,.2f}")
