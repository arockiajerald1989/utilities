import re
import os
import json
from typing import Optional

class TreeSearcher:

    def __init__(self, json_file_path, search_path, regex_pattern, search_for="files", file_size_filter=None, max_depth: Optional[int] = None):
        """
        Initialize the TreeSearcher class with necessary parameters.

        :param json_file_path: Path to the JSON file
        :param search_path: Absolute path to search within the JSON tree
        :param regex_pattern: Regular expression pattern for searching files or directories
        :param search_for: Can be 'files', 'directories', or 'both'
        :param file_size_filter: Optional size filter (e.g., '500KB') for filtering files by size
        :param max_depth: Optional integer to limit the search depth
        """
        self.json_file_path = json_file_path
        self.search_path = search_path
        self.regex_pattern = re.compile(regex_pattern)
        self.search_for = search_for
        self.file_size_filter = file_size_filter
        self.max_depth = max_depth  # Depth control parameter
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

    def search_files_recursively(self, node, current_depth=0):
        """Recursively search for files and/or directories matching the regex pattern with depth control."""

        # If the node is empty or we have exceeded the max depth, stop recursion
        if not node or (self.max_depth is not None and current_depth > self.max_depth):
            return
        
        # Check for directories if required, but only within the allowed depth
        if self.search_for in ['directories', 'both'] and 'directories' in node and current_depth <= self.max_depth:
            for directory in node['directories']:
                dir_name, dir_size = directory

                # Apply regex to directory names
                if self.regex_pattern.match(dir_name):
                    if self.file_size_filter and dir_size != self.file_size_filter:
                        continue  # Skip directories that don't match the size filter
                    absolute_dir_path = os.path.join(node['absolute_path'], dir_name)
                    self.matching_directories.append((absolute_dir_path, dir_size))

                # Continue searching within the directory, increasing depth
                dir_node = node.get(dir_name, None)
                if dir_node:
                    self.search_files_recursively(dir_node, current_depth + 1)

        # Check for files if required, but only within the allowed depth
        if self.search_for in ['files', 'both'] and 'files' in node and current_depth <= self.max_depth:
            for file in node['files']:
                file_name, file_size = file

                # Apply regex and size filter (if provided)
                if self.regex_pattern.match(file_name):
                    if self.file_size_filter and file_size != self.file_size_filter:
                        continue  # Skip files that don't match the size filter
                    absolute_file_path = os.path.join(node['absolute_path'], file_name)
                    self.matching_files.append((absolute_file_path, file_size))

    def search_directory(self):
        """Search the JSON tree for files or directories based on the regex pattern."""
        if "devices" not in self.json_data:
            print("Error: 'devices' node not found in the JSON.")
            return

        devices_node = self.json_data["devices"]
        root = self.find_node_by_absolute_path(devices_node, self.search_path)

        if root:
            self.search_files_recursively(root, current_depth=0)
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


# Sample Usage
regex_pattern = r'document_.*\.pdf$'
search_path = "C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices"

# Create an instance of the TreeSearcher class with max_depth=0
tree_searcher = TreeSearcher(
    json_file_path=os.path.join('path_tree', 'tree.json'),
    search_path=search_path,
    regex_pattern=regex_pattern,
    search_for="files",  # Search only for files
    file_size_filter="500KB",  # Filter files of size '500KB'
    max_depth=0  # Limit search to the first level only
)

# Perform the search
if tree_searcher.json_data:
    tree_searcher.search_directory()
    tree_searcher.display_results()
else:
    print("Failed to load or process the JSON data.")
