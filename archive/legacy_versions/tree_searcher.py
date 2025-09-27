import re
import os
import json

class TreeSearcher:

    def __init__(self, json_file_path, search_path, regex_pattern, search_for="files", file_size_filter=None):
        """
        Initialize the TreeSearcher class with necessary parameters.

        :param json_file_path: Path to the JSON file
        :param search_path: Absolute path to search within the JSON tree
        :param regex_pattern: Regular expression pattern for searching files or directories
        :param search_for: Can be 'files', 'directories', or 'both'
        :param file_size_filter: Optional size filter (e.g., '500KB') for filtering files by size
        """
        self.json_file_path = json_file_path
        self.search_path = search_path
        self.regex_pattern = re.compile(regex_pattern)
        self.search_for = search_for
        self.file_size_filter = file_size_filter  # Optional size filter
        self.matching_files = []
        self.matching_directories = []
        self.json_data = self.load_json()

    def load_json(self):
        """Load the JSON data from the specified file."""
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.json_file_path} was not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.json_file_path}.")
            return {}

    def find_node_by_absolute_path(self, node, search_path):
        """Recursively find the node with the given absolute path."""
        if node.get('absolute_path') == search_path:
            return node

        if 'directories' in node:
            for directory in node['directories']:
                dir_name = directory[0]
                if dir_name in node:
                    dir_node = node[dir_name]
                    result = self.find_node_by_absolute_path(dir_node, search_path)
                    if result:
                        return result
        return None

    def search_files_recursively(self, node):
        """Recursively search for files and/or directories matching the regex pattern."""
        if 'files' in node:
            for file in node['files']:
                file_name, file_size = file

                # Apply regex and size filter (if provided)
                if self.regex_pattern.match(file_name):
                    if self.file_size_filter and file_size != self.file_size_filter:
                        continue  # Skip files that don't match the size filter
                    absolute_file_path = os.path.join(node['absolute_path'], file_name)
                    self.matching_files.append((absolute_file_path, file_size))

        # Recursively check directories
        if 'directories' in node:
            for directory in node['directories']:
                dir_name = directory[0]
                if dir_name in node:
                    dir_node = node[dir_name]
                    self.search_files_recursively(dir_node)

    def search_directory(self):
        """Search the JSON tree for files or directories based on the regex pattern."""
        if "devices" not in self.json_data:
            print("Error: 'devices' node not found in the JSON.")
            return

        devices_node = self.json_data["devices"]
        root = self.find_node_by_absolute_path(devices_node, self.search_path)

        if root:
            self.search_files_recursively(root)
        else:
            print(f"No matching node found for {self.search_path}")

    def display_results(self):
        """Display the matching files and directories."""
        if self.search_for in ['directories', 'both'] and self.matching_directories:
            print("Matching Directories:")
            for dir_path, dir_size in self.matching_directories:
                print(f"Directory: {dir_path}, Size: {dir_size}")

        if self.search_for in ['files', 'both'] and self.matching_files:
            print("\nMatching Files:")
            for file_path, file_size in self.matching_files:
                print(f"File: {file_path}, Size: {file_size}")

        if not self.matching_files and self.search_for in ['files', 'both']:
            print("No matching files found.")


# === USAGE SUMMARY ===
# Below are some example regex patterns and search scenarios to guide usage:

# 1. Match files that start with 'document_' and end with '.pdf'
#    regex_pattern = r'document_.*\.pdf$'
#    Explanation: Matches any file starting with 'document_' and ending with '.pdf', no matter what comes between.
#    Example: 'document_202307301301.pdf', 'document_report_20230730.pdf'

# 2. Match files with exactly 8 digits between 'document_' and '.pdf'
#    regex_pattern = r'document_\d{8}\.pdf$'
#    Explanation: Matches files with exactly 8 digits (e.g., a date format like YYYYMMDD) between 'document_' and '.pdf'.
#    Example: 'document_20230730.pdf', but not 'document_202307301301.pdf'.

# 3. Match files with alphanumeric text and digits after 'document_'
#    regex_pattern = r'document_\w+_\d+\.pdf$'
#    Explanation: Matches files where 'document_' is followed by alphanumeric text, digits, and ends with '.pdf'.
#    Example: 'document_report_20230730.pdf'

# 4. Match files containing the word 'report' between 'document_' and digits, ending with '.pdf'
#    regex_pattern = r'document_report_\d+\.pdf$'
#    Explanation: Matches files containing the word 'report' between 'document_' and digits, ending with '.pdf'.
#    Example: 'document_report_20230730.pdf'

# 5. Match all '.pdf' files
#    regex_pattern = r'.*\.pdf$'
#    Explanation: Matches all '.pdf' files regardless of the prefix or pattern before '.pdf'.
#    Example: 'document_202307301301.pdf', 'summary_202307301229.pdf'

# 6. Match files starting with 'test_' and ending with '.txt'
#    regex_pattern = r'test_.*\.txt$'
#    Explanation: Matches files starting with 'test_' and ending with '.txt'.
#    Example: 'test_sample_20230730.txt', 'test_config.txt'

# 7. Match files with a specific size (e.g., 500KB)
#    regex_pattern = r'document_.*\.pdf$'
#    file_size_filter = '500KB'
#    Explanation: Matches '.pdf' files that are exactly 500KB in size.
#    Example: 'document_202307301301.pdf' that is exactly 500KB.

# === END OF USAGE SUMMARY ===


# === SAMPLE USAGE EXAMPLE ===
# Define the regex pattern for the search
regex_pattern = r'document_.*\.pdf$'
search_path = "C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices"


# Create an instance of the TreeSearcher class
tree_searcher = TreeSearcher(
    json_file_path=os.path.join(os.getcwd(), 'path_tree', 'tree.json'),
    search_path=search_path,
    regex_pattern=regex_pattern,
    search_for="files",
    file_size_filter="500KB"  # Optional: Set to '500KB' for size-based filtering
)

# Perform the search
if tree_searcher.json_data:
    tree_searcher.search_directory()
    tree_searcher.display_results()
else:
    print("Failed to load or process the JSON data.")
