# Utilities Repository

## Overview

This repository contains a collection of Python utilities for data processing, file analysis, and automation tasks. The utilities include Excel data processing, Git operations, file system analysis, log processing, and more.

## Repository Structure

### `git-tools/`
Git repository management and operations
- **git_operations.py** - Comprehensive Git repository manager
- **git_branch_utils.py** - Git branch detection utility
- **git_advanced_manager.py** - Advanced Git manager with caching/logging
- **git_repository_manager.py** - Enhanced Git manager with documentation
- **repo_validator.py** - JSON repository config validator

### `data-processing/`
Data analysis and processing utilities
- **multibagger_stocks.py** - Stock market analysis with technical indicators
- **multiline_log_processor.py** - JSON log processor for timestamped data

### `api-integration/`
API clients and external service integration
- **task_api_client.py** - REST API client for task management
- **splunk_hec_client.py** - Splunk HEC plugin for JSON data posting

### `file-system/`
File system navigation and search utilities
- **tree_searcher.py** - File system search with regex/depth control
- **interim_file_latest.py** - Advanced TreeSearcher with test cases
- **search_payload_json.py** - Wildcard-based JSON file search
- **path_tree_with_os.py** - Directory tree structure generator
- **path_tree.json** - Sample directory tree data
- **path_tree.sh** - Bash script for JSON directory trees

### `business-tools/`
Business process automation and HR tools
- **employee_records_missing_info.py** - HR documentation analyzer
- **payroll_calculator.py** - Payroll with overtime/shift calculations
- **invoice_creation.py** - Invoice generator with pivot tables
- **timesheet_analyzer.py** - Timesheet processor
- **xls_file_parser.py** - Excel timesheet parser
- **xlsfileparser_tk.py** - TK-specific Excel parser
- **floor2plan.py** - Web scraping automation for timesheets
- **compare_sheets.py** - Excel comparison for FTP/TS business data
- **ftp_vs_ts_comparison.py** - Business data comparison with pivot tables

### `samples/`
Code samples and template files
- **tree_searcher_sample.py** - TreeSearcher class sample implementation
- **git_clone_sample.py** - Git cloning function snippet

### `archive/`
Legacy versions and deprecated utilities that have been superseded by enhanced implementations. See `archive/README.md` for detailed information about archived files.

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
