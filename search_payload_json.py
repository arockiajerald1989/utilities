import json

# Define the search parameters
search_path = "devices"
prefix_file_name = "document"
suffix_file_name = ".pdf"

# Load the JSON data from a file
with open('path_tree.json', 'r') as file:
    json_data = json.load(file)


def search_files_recursively(node, prefix, suffix, current_path, matching_files):
    # Check files at the current node
    if 'files' in node:
        for file in node['files']:
            if file[0].startswith(prefix) and file[0].endswith(suffix):
                absolute_file_path = current_path + "\\" + file[0]
                matching_files.append((absolute_file_path, file[1]))

    # Recursively search in child directories
    if 'directories' in node:
        for directory in node['directories']:
            dir_name = directory[0]
            if dir_name in node:
                search_files_recursively(node[dir_name], prefix, suffix, current_path + "\\" + dir_name, matching_files)


def find_node(data, path):
    if path in data:
        return data[path]
    for k, v in data.items():
        if isinstance(v, dict):
            result = find_node(v, path)
            if result:
                return result
    return None


def search_directory(data, search_path, prefix, suffix):
    root = find_node(data, search_path)
    if root:
        matching_files = []
        search_files_recursively(root, prefix, suffix, root['absolute_path'], matching_files)
        return matching_files
    else:
        return []


matching_files = search_directory(json_data, search_path, prefix_file_name, suffix_file_name)
for file_path, file_size in matching_files:
    print(f"File: {file_path}, Size: {file_size}")
