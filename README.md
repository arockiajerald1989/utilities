## Overview

This Python script extracts, processes, and restructures data from an Excel file, generating a new, well-formatted Excel file for further analysis and utilization.

## Key Functionalities:

- Imports Data using Pandas
- Extracts and Separates Information using regular expressions
- Rearranges Columns
- Calculates Regular and Overtime Hours
- Writes to New Excel File with auto-formatted column widths
## Installation Requirements:

- Python (version 3.6 or later)
- Libraries:
  * pandas
  * openpyxl
## Usage Instructions:

1. Install Required Libraries:
   
   ``` pip install pandas openpyxl ```
   
2. Confirm Input File Name:
    - Within the script, verify that the output_file.xlsx placeholder aligns with your input file name.
    
3. Execute the Script:

    ``` python extract_data.py  # Replace with the actual script filename ```

4. Access Processed Data:
   - The generated output file, extracted_data.xlsx, will contain the parsed and formatted data.
## Additional Customization:

* Modify the regular expression in the str.extract method to match your data structure.
* Adjust column names and order in the df[['Name', 'Number', ...]] section.
* Change the overtime threshold in the overtime_threshold variable if needed.
