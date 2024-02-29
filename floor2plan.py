import glob
import os
import shutil
import time

import openpyxl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

url = "https://philly.floor2plan.com/Account/Login"  # Replace with your desired URL
driver.get(url)
driver.maximize_window()

# Locate username and password fields (adjust locators as needed)
username_field = driver.find_element(By.ID, "userName")
password_field = driver.find_element(By.ID, "password")

# Replace with your actual credentials
# username = "49772"
# password = "234"

# Enter username and password
username_field.send_keys(username)
password_field.send_keys(password)

# Submit the form (adjust the locator as needed)
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

report_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Reports')]")
report_button[1].click()
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Hours']"))
)
element.click()
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Weekly Timesheet Report")]'))
)
element.click()

dropdown_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[@class='k-input-value-text']")))
dropdown_button.click()

search_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@role='searchbox']")))
search_field.send_keys("102")

option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '102')]"))  # Replace with appropriate locator
)
option.click()

report_button = driver.find_elements(By.XPATH, "//input[@data-role='datepicker']")
report_button[1].clear()
report_button[2].clear()
report_button[1].send_keys("02/19/2024")
report_button[2].send_keys("02/25/2024")
option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Generate']"))  # Replace with appropriate locator
)
option.click()
option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Export to Excel']"))
)
option.click()
time.sleep(3)
download_path = os.path.expanduser("~\\Downloads")  # Expands path to user's Downloads folder
files = sorted(os.listdir(download_path), key=lambda f: os.path.getmtime(os.path.join(download_path, f)), reverse=True)
last_downloaded_file = os.path.join(download_path, files[0])
filenames = glob.glob("." + "*.xlsx")
for i in filenames:
    os.remove(i)
shutil.move(last_downloaded_file, 'data.xlsx')
shutil.copy("data.xlsx", "data-final.xlsx")

# Load the Excel workbook
workbook = openpyxl.load_workbook("data-final.xlsx")

# Select the worksheet
worksheet = workbook["Sheet1"]  # Replace with your sheet name

# Delete a specific row (index starts from 1)
worksheet.delete_rows(idx=1)  # Delete row 3

# Save the modified workbook
workbook.save("data-final.xlsx")

# Load Excel data into a DataFrame
df = pd.read_excel('data-final.xlsx', sheet_name='Sheet1')
# Extract names and numbers using regular expressions
df[['FullName', 'ID']] = df['name'].str.extract(r"(.*) \((\d+)\)")
df = df.drop('name', axis=1)  # Drop the original 'won' column

df['Project'] = df['won'].str[:4]  # Keep only first 3 for Project
df['Team'] = df['won'].str[-3:]  # Keep only last 3 for Team

# Create pivot table
pivot_table = df.pivot_table(values='jobTime',
                             index='ID',
                             columns='date',
                             aggfunc='sum', fill_value=0)  # Customize aggregation function

pivot_table['Total Hours'] = pivot_table.sum(axis=1)

# Group and concatenate unique Project and Team data
project_data = df.groupby('ID')['Project'].apply(lambda x: ','.join(set(x.astype(str))))
team_data = df.groupby('ID')['Team'].apply(lambda x: ','.join(set(x.astype(str))))
test = df.groupby('ID')['FullName'].apply(lambda x: ','.join(set(x.astype(str))))

# Merge unique Project and Team data into the pivot table
pivot_table = pivot_table.merge(project_data, on='ID', how='left')
pivot_table = pivot_table.merge(team_data, on='ID', how='left')
pivot_table = pivot_table.merge(test, on='ID', how='left')

# Create an Excel writer with openpyxl
writer = pd.ExcelWriter('output_file.xlsx', engine='openpyxl')
pivot_table.to_excel(writer, sheet_name='TimeAndMaterial')

# Access the workbook and worksheet
workbook = writer.book
worksheet = writer.sheets['TimeAndMaterial']

# Autofit all columns
for column in worksheet.columns:
    worksheet.column_dimensions[column[1].column_letter].auto_size = True

# Save the Excel file
writer.close()

# Load the Excel file
df = pd.read_excel('output_file.xlsx')

column_length = len(df.columns)

# Extract regular and overtime hours
overtime_threshold = 40
df['Regular Hours'] = df['Total Hours'].clip(upper=overtime_threshold)
df['Overtime Hours'] = df['Total Hours'] - df['Regular Hours']

# Add the 'No of Days' column
df['No of Days >= 6.0'] = 0

# Calculate the count of days for each row
for index, row in df.iterrows():
    for column in list(df.columns[1:8]):
       if row[column] >= 6.0:
           df.loc[index, 'No of Days >= 6.0'] += 1

df = df[['FullName', 'ID', 'Project', 'Team'] + list(df.columns[1:column_length-4]) + ['Total Hours', 'Regular Hours', 'Overtime Hours', 'No of Days >= 6.0']]

# Sort by 'FullName'
df = df.sort_values(by='FullName')
df.to_excel('FTP.xlsx', index=False)

# Reopen the Excel file for formatting
workbook = openpyxl.load_workbook('FTP.xlsx')
worksheet = workbook.active

# Autofit columns
for column in worksheet.columns:
    worksheet.column_dimensions['A'].width = 30
    worksheet.column_dimensions[column[1].column_letter].auto_size = True

# Save the formatted workbook
workbook.save('FTP.xlsx')
