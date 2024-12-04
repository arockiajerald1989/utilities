import re
import os
import json
from typing import Optional


class TreeSearcher:
    def __init__(
        self,
        json_file_path: str,
        search_path: str,
        regex_pattern: str,
        search_for: str = "files",
        max_depth: Optional[int] = None,
        file_size_filter: Optional[int] = None,
        flags: int = 0
    ):
        self.json_file_path = json_file_path
        self.search_path = search_path
        self.regex_pattern = re.compile(regex_pattern, flags)
        self.search_for = search_for
        self.max_depth = max_depth
        self.file_size_filter = file_size_filter
        self.matching_files = []
        self.matching_directories = []
        self.json_data = self.load_json()

    def load_json(self) -> Optional[dict]:
        print(f"Attempting to load JSON from: {self.json_file_path}")
        if not os.path.exists(self.json_file_path):
            print(f"Error: The file {self.json_file_path} does not exist.")
            return None
        try:
            with open(self.json_file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error: Could not decode JSON. Details: {e}")
            return None

    def validate_json_structure(self, node: dict) -> bool:
        required_keys = ['absolute_path', 'directories', 'files']
        for key in required_keys:
            if key not in node:
                print(f"Error: Missing key '{key}' in JSON node.")
                return False
        return True

    def find_node_by_absolute_path(self, node: dict, search_path: str) -> Optional[dict]:
        if not isinstance(node, dict):
            return None
        if node.get('absolute_path') == search_path:
            return node
        if 'directories' in node:
            for directory in node['directories']:
                dir_name, _ = directory
                dir_node = node.get(dir_name, {})
                result = self.find_node_by_absolute_path(dir_node, search_path)
                if result:
                    return result
        return None

    def search_files_recursively(self, node: dict, current_depth: int = 0):
        if not node:
            return

        if self.max_depth is not None and current_depth > self.max_depth:
            return

        if 'directories' in node:
            for directory in node['directories']:
                dir_name, dir_size = directory
                dir_node = node.get(dir_name, {})

                if self.search_for in ['directories', 'both'] and self.regex_pattern.match(dir_name):
                    absolute_dir_path = os.path.join(node['absolute_path'], dir_name)
                    self.matching_directories.append((absolute_dir_path, dir_size))

                self.search_files_recursively(dir_node, current_depth + 1)

        if self.search_for in ['files', 'both'] and 'files' in node:
            for file in node['files']:
                file_name, file_size = file
                if self.regex_pattern.match(file_name):
                    absolute_file_path = os.path.join(node['absolute_path'], file_name)
                    self.matching_files.append((absolute_file_path, file_size))

    def apply_filters(self):
        if self.file_size_filter:
            self.matching_files = [
                (path, size) for path, size in self.matching_files
                if convert_size_to_bytes(size) > self.file_size_filter
            ]

    def search_directory(self):
        if not self.json_data or "devices" not in self.json_data:
            print("Error: 'devices' node not found in the JSON.")
            return

        devices_node = self.json_data["devices"]
        root = self.find_node_by_absolute_path(devices_node, self.search_path)

        if root:
            if not self.validate_json_structure(root):
                print("Error: Invalid JSON structure.")
                return
            self.search_files_recursively(root, current_depth=0)
        else:
            print(f"No matching node found for {self.search_path}")

    def display_results(self):
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
        if not self.matching_directories and self.search_for in ['directories', 'both']:
            print("No matching directories found.")

    def save_results(self, output_file: str = "results.json"):
        results = {
            "matching_files": self.matching_files,
            "matching_directories": self.matching_directories
        }
        try:
            with open(output_file, 'w') as file:
                json.dump(results, file, indent=4)
            print(f"Results saved to {output_file}")
        except IOError as e:
            print(f"Error saving results to {output_file}. Details: {e}")


def convert_size_to_bytes(size: str) -> int:
    size = size.upper().strip()
    if "KB" in size:
        return int(size.replace("KB", "")) * 1024
    elif "MB" in size:
        return int(size.replace("MB", "")) * 1024 * 1024
    elif "GB" in size:
        return int(size.replace("GB", "")) * 1024 * 1024 * 1024
    return int(size)


# Enhanced Test Cases for the Provided JSON Structure
# Extended Test Cases
test_cases = [
    {"description": "Files starting with 'log'.", "search_for": "files", "regex_pattern": r'^log.*', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Directories starting with 'devices_'.", "search_for": "directories", "regex_pattern": r'^devices_.*', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Case-insensitive files starting with 'readme'.", "search_for": "files", "regex_pattern": r'^readme.*', "max_depth": None, "flags": re.IGNORECASE, "file_size_filter": None},
    {"description": "Files larger than 1MB.", "search_for": "files", "regex_pattern": r'.*', "max_depth": None, "flags": 0, "file_size_filter": 1 * 1024 * 1024},
    {"description": "Files matching 'document_*' up to depth 4.", "search_for": "files", "regex_pattern": r'^document.*', "max_depth": 4, "flags": 0, "file_size_filter": None},
    {"description": "Both files and directories starting with 'test'.", "search_for": "both", "regex_pattern": r'^test.*', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Files with '.pdf' extension.", "search_for": "files", "regex_pattern": r'.*\.pdf$', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Files and directories containing 'subtest'.", "search_for": "both", "regex_pattern": r'.*subtest.*', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Files with extensions '.doc' or '.docx'.", "search_for": "files", "regex_pattern": r'.*\.(doc|docx)$', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Files containing 'data' larger than 1MB.", "search_for": "files", "regex_pattern": r'.*data.*', "max_depth": None, "flags": 0, "file_size_filter": 1 * 1024 * 1024},
    {"description": "Deeply nested '.txt' files (depth 6).", "search_for": "files", "regex_pattern": r'.*\.txt$', "max_depth": 6, "flags": 0, "file_size_filter": None},
    {"description": "Files containing 'outline'.", "search_for": "files", "regex_pattern": r'.*outline.*', "max_depth": None, "flags": 0, "file_size_filter": None},
    {"description": "Directories at depth 2.", "search_for": "directories", "regex_pattern": r'.*', "max_depth": 2, "flags": 0, "file_size_filter": None},
]

# Execute Extended Test Cases
for i, case in enumerate(test_cases, 1):
    print(f"\nRunning Test Case {i}: {case['description']}")
    tree_searcher = TreeSearcher(
        json_file_path=r"C:\Users\T14 Windows 11\PycharmProjects\path_tree\working_models\tree.json",
        search_path="C:\\Users\\T14 Windows 11\\PycharmProjects\\path_tree\\devices",
        regex_pattern=case["regex_pattern"],
        search_for=case["search_for"],
        max_depth=case["max_depth"],
        file_size_filter=case.get("file_size_filter"),
        flags=case.get("flags", 0),
    )
    tree_searcher.search_directory()
    tree_searcher.apply_filters()
    tree_searcher.display_results()
    tree_searcher.save_results(output_file=f"results_case_{i}.json")
    print(f"Results for Test Case {i} saved to results_case_{i}.json")
