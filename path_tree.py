import os


def create_path_tree(root_dir):
  """
  Creates a dictionary representing the path tree of a directory.

  Args:
      root_dir: The root directory path (string).

  Returns:
      A dictionary representing the path tree with the following structure:
          {
              'folder_name': {
                  # If folder is empty: None
                  'files': [],  # List of filenames
                  'children': {  # Dictionary for subfolders
                      'subfolder1_name': {...},
                      # ...
                  }
              },
              # ... other folders in root_dir
          }
  """

  tree = {}
  for item in os.listdir(root_dir):
    item_path = os.path.join(root_dir, item)
    if os.path.isfile(item_path):
      tree.setdefault(item, []).append(item)  # Append filename to list
    else:
      child_tree = create_path_tree(item_path)  # Recursively create subtree
      if child_tree:  # Add subtree only if it's not empty
        tree[item] = {'files': [], 'children': child_tree}

  return tree


if __name__ == '__main__':
  root_path = '/path/to/your/directory'  # Replace with your root directory
  path_tree = create_path_tree(root_path)
  print(path_tree)
