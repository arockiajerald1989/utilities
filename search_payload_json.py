import json
import os
import fnmatch

# Define the search parameters
search_path = "C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices"  # Full absolute path from the tree.json
wildcard_pattern = "test_?"  # Wildcard pattern to search for in filenames or directories
search_for = "files"  # Can be 'files', 'directories', or 'both'

# Load the JSON data from a file with error handling
file_path = os.path.join(os.getcwd(), 'path_tree', 'tree.json')
try:
    with open(file_path, 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    json_data = {}
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {file_path}.")
    json_data = {}


def search_files_recursively(node, wildcard_pattern, matching_files, matching_directories, search_for):
    """
    Recursively search for files and/or directories in the current node and all subdirectories
    that match the wildcard pattern.
    """
    # Check files in the current node
    if search_for in ['files', 'both'] and 'files' in node:
        for file in node['files']:
            file_name, file_size = file
            if fnmatch.fnmatch(file_name, wildcard_pattern):
                absolute_file_path = os.path.join(node['absolute_path'], file_name)
                matching_files.append((absolute_file_path, file_size))

    # Check directories in the current node
    if search_for in ['directories', 'both'] and 'directories' in node:
        for directory in node['directories']:
            dir_name = directory[0]
            dir_size = directory[1]
            # Check if directory matches the wildcard pattern
            if fnmatch.fnmatch(dir_name, wildcard_pattern):
                absolute_directory_path = os.path.join(node['absolute_path'], dir_name)
                matching_directories.append((absolute_directory_path, dir_size))

            # Recursively search in subdirectories
            if dir_name in node:  # Ensure the directory node exists
                dir_node = node[dir_name]
                search_files_recursively(dir_node, wildcard_pattern, matching_files, matching_directories, search_for)


def find_node_by_absolute_path(node, search_path):
    """
    Recursively find the node with the given absolute path.
    """
    # Check if this node has the matching absolute_path
    if node.get('absolute_path') == search_path:
        return node

    # Search through child directories
    if 'directories' in node:
        for directory in node['directories']:
            dir_name = directory[0]
            if dir_name in node:  # Check if the directory node exists
                dir_node = node[dir_name]
                result = find_node_by_absolute_path(dir_node, search_path)  # Recursively search for the absolute path
                if result:
                    return result
    return None


def search_directory(data, search_path, wildcard_pattern, search_for):
    # Begin the search within the "devices" node in the JSON
    if "devices" not in data:
        print("Error: 'devices' node not found in the JSON.")
        return [], []

    # Start the search from the "devices" node
    devices_node = data["devices"]

    # Find the node that matches the absolute path
    root = find_node_by_absolute_path(devices_node, search_path)
    matching_files = []
    matching_directories = []

    if root:
        search_files_recursively(root, wildcard_pattern, matching_files, matching_directories, search_for)
    else:
        print(f"No matching node found for {search_path}")

    return matching_files, matching_directories


# Perform the search if json_data was successfully loaded
if json_data:
    matching_files, matching_directories = search_directory(json_data, search_path, wildcard_pattern, search_for)

    # Print matching directories and sizes
    if search_for in ['directories', 'both'] and matching_directories:
        print("Matching Directories:")
        for dir_path, dir_size in matching_directories:
            print(f"Directory: {dir_path}, Size: {dir_size}")
    elif search_for == 'directories':
        print("No matching directories found.")

    # Print matching files and sizes
    if search_for in ['files', 'both'] and matching_files:
        print("\nMatching Files:")
        for file_path, file_size in matching_files:
            print(f"File: {file_path}, Size: {file_size}")
    elif search_for == 'files':
        print("No matching files found.")
else:
    print("Failed to load or process the JSON data.")
