import json
import os
import fnmatch


class TreeSearcher:

    def __init__(self, json_file_path, search_path, wildcard_pattern, search_for="files"):
        """
        Initialize the TreeSearcher class with necessary parameters.

        :param json_file_path: Path to the JSON file
        :param search_path: Absolute path to search within the JSON tree
        :param wildcard_pattern: Wildcard pattern for searching files or directories
        :param search_for: Can be 'files', 'directories', or 'both'
        """
        self.json_file_path = json_file_path
        self.search_path = search_path
        self.wildcard_pattern = wildcard_pattern
        self.search_for = search_for
        self.json_data = self.load_json()
        self.matching_files = []
        self.matching_directories = []

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
        """
        Recursively find the node with the given absolute path.
        """
        if node.get('absolute_path') == search_path:
            return node

        if 'directories' in node:
            for directory in node['directories']:
                dir_name = directory[0]
                if dir_name in node:  # Check if the directory node exists
                    dir_node = node[dir_name]
                    result = self.find_node_by_absolute_path(dir_node, search_path)
                    if result:
                        return result
        return None

    def search_files_recursively(self, node):
        """
        Recursively search for files and/or directories in the current node and all subdirectories
        that match the wildcard pattern.
        """
        # Check files in the current node
        if self.search_for in ['files', 'both'] and 'files' in node:
            for file in node['files']:
                file_name, file_size = file
                if fnmatch.fnmatch(file_name, self.wildcard_pattern):
                    absolute_file_path = os.path.join(node['absolute_path'], file_name)
                    self.matching_files.append((absolute_file_path, file_size))

        # Check directories in the current node
        if self.search_for in ['directories', 'both'] and 'directories' in node:
            for directory in node['directories']:
                dir_name = directory[0]
                dir_size = directory[1]
                if fnmatch.fnmatch(dir_name, self.wildcard_pattern):
                    absolute_directory_path = os.path.join(node['absolute_path'], dir_name)
                    self.matching_directories.append((absolute_directory_path, dir_size))

                if dir_name in node:  # Recursively search in subdirectories
                    dir_node = node[dir_name]
                    self.search_files_recursively(dir_node)

    def search_directory(self):
        """
        Search the JSON tree for files or directories based on the wildcard pattern.
        """
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
        """
        Display the matching files and directories.
        """
        if self.search_for in ['directories', 'both'] and self.matching_directories:
            print("Matching Directories:")
            for dir_path, dir_size in self.matching_directories:
                print(f"Directory: {dir_path}, Size: {dir_size}")
        elif self.search_for == 'directories':
            print("No matching directories found.")

        if self.search_for in ['files', 'both'] and self.matching_files:
            print("\nMatching Files:")
            for file_path, file_size in self.matching_files:
                print(f"File: {file_path}, Size: {file_size}")
        elif self.search_for == 'files':
            print("No matching files found.")


# Define the search parameters
json_file_path = os.path.join(os.getcwd(), 'path_tree', 'tree.json')
search_path = "C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices"
wildcard_pattern = "test*"  # Wildcard pattern to search for in filenames or directories
search_for = "both"  # Can be 'files', 'directories', or 'both'

# Create an instance of the TreeSearcher class
tree_searcher = TreeSearcher(json_file_path, search_path, wildcard_pattern, search_for)

# Perform the search
if tree_searcher.json_data:
    tree_searcher.search_directory()
    tree_searcher.display_results()
else:
    print("Failed to load or process the JSON data.")
