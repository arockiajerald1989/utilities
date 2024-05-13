import os
import pprint


def create_path_tree(folder_path):
    # Get the base name of the current path
    base_name = os.path.basename(folder_path)

    # Initialize the path tree with base name as key
    path_tree = {
        base_name: {
            'absolute_path': os.path.abspath(folder_path),
            'files': [],
            'directories': []
        }
    }

    # Initialize lists for files and directories
    files_list = []
    directories_list = []

    # Iterate over the contents of the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            files_list.append(item)
        elif os.path.isdir(item_path):
            directories_list.append(item)

    # Add files and directories to the dictionary
    path_tree[base_name]['files'] = files_list
    path_tree[base_name]['directories'] = directories_list

    # Recursively create path trees for subdirectories
    for directory in directories_list:
        subdirectory_path = os.path.join(folder_path, directory)
        # Update the path_tree dictionary with the subdirectory structure
        path_tree[base_name][directory] = create_path_tree(subdirectory_path)[directory]

    return path_tree

# Example usage:
folder_path = 'C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices'
path_tree = create_path_tree(folder_path)

# Pretty print the path tree
pprint.pprint(path_tree)
