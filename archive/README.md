# Archive Directory

This directory contains archived versions of utilities that have been superseded by newer implementations or represent alternative approaches to solving the same problems.

## Directory Structure

### `/legacy_versions/`
Contains older versions of utilities that have been superseded by enhanced implementations.

- **Interim_file** - Legacy version of TreeSearcher class
  - **Current Version**: `interim_file_latest.py`
  - **Archived**: Contains older implementation with hardcoded test cases
  - **Reason**: Superseded by version with better error handling and type hints

- **Test1** - Simplified version of GitRepositoryManager
  - **Current Version**: `Test`
  - **Archived**: Basic implementation (122 lines)
  - **Reason**: Superseded by full-featured version with logging, caching, and retry logic

- **log_processor** - Basic JSON log extractor
  - **Current Version**: `Multiline_log_processor`
  - **Archived**: Single-line JSON handling only
  - **Reason**: Superseded by enhanced version supporting multiline JSON

- **tree_searcher.py** - Basic TreeSearcher implementation
  - **Current Version**: `TreeSearcher`
  - **Archived**: No depth control feature
  - **Reason**: Superseded by version with max_depth parameter

### `/alternative_implementations/`
Contains alternative approaches to solving the same problems as current utilities.

- **path_tree_without_os** - Complex directory tree generator
  - **Current Version**: `path_tree_with_os.py`
  - **Archived**: Complex implementation with subprocess calls
  - **Reason**: Simpler, cleaner implementation preferred

### `/deprecated/`
Contains utilities with duplicate functionality that have been consolidated.

- **xlsfileparser_tm.py** - Excel parser for TS files
  - **Current Version**: `xlsfileparser_tk.py` (can be configured for different inputs)
  - **Archived**: Nearly identical code, different input source
  - **Reason**: Functionality consolidated into configurable version

- **compare_ts_versions.py** - Timesheet version comparison
  - **Current Version**: `ftp_vs_ts_comparison.py` (can be configured for different comparisons)
  - **Archived**: Nearly identical comparison logic
  - **Reason**: Functionality consolidated into configurable version

- **compare_ftp_versions.py** - FTP version comparison
  - **Current Version**: `ftp_vs_ts_comparison.py` (can be configured for different comparisons)
  - **Archived**: Nearly identical comparison logic
  - **Reason**: Functionality consolidated into configurable version

## Archive Policy

### When files are archived:
1. **Legacy Versions**: When a utility is significantly enhanced or refactored
2. **Alternative Implementations**: When a simpler or more maintainable approach is adopted
3. **Deprecated**: When duplicate functionality is consolidated

### Archive Retention:
- Files are preserved for historical reference and potential feature extraction
- No active maintenance is performed on archived files
- Archived files maintain their original structure and comments

## Usage Guidelines

### Accessing Archived Files:
- For reference purposes only
- May contain outdated dependencies or practices
- Not recommended for production use

### Restoration Process:
If you need to restore functionality from archived files:
1. Review the current implementation first
2. Identify specific features needed from the archive
3. Integrate features into the current version rather than restoring the entire file
4. Update dependencies and coding standards as needed

---
*Last Updated: September 2025*
*Archive created during repository cleanup and organization*