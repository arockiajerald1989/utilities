import json
import re

class JSONValidator:
    def __init__(self, json_input):
        self.json_input = json_input
        self.data = None

    # Function to load the JSON
    def load_json(self):
        try:
            self.data = json.loads(self.json_input)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

    # Function to validate the top-level structure and repositories
    def validate_json(self):
        self.load_json()

        repositories = self.data.get('repositories', None)
        if not isinstance(repositories, list) or len(repositories) == 0:
            raise ValueError("Invalid JSON structure: 'repositories' field is missing or not a non-empty list.")

        # Loop through repositories and validate them
        for index, repo in enumerate(repositories):
            self.validate_repository(repo, index)

        return self.data

    # Function to validate each repository entry
    def validate_repository(self, repo, index):
        # Validate that it's a dictionary
        if not isinstance(repo, dict):
            raise ValueError(f"Invalid repository entry at index {index}: Each repository must be an object. Found: {type(repo)}")

        # Validate that it only contains 'name' and 'branch' fields
        valid_keys = {'name', 'branch'}
        if set(repo.keys()) != valid_keys:
            raise ValueError(f"Invalid repository at index {index}: Unexpected keys found. Only 'name' and 'branch' are allowed.")

        # Validate the 'name' and 'branch' fields
        if not isinstance(repo['name'], str) or not isinstance(repo['branch'], str):
            raise ValueError(f"Invalid repository at index {index}: 'name' and 'branch' must be strings.")

        # Strip once and validate
        name = repo['name'].strip()
        branch = repo['branch'].strip()

        if not name:
            raise ValueError(f"Invalid repository name at index {index}: Repository 'name' must be a non-empty string.")
        
        if not branch:
            raise ValueError(f"Invalid branch name at index {index}: Repository 'branch' must be a non-empty string.")

        # Additional regex validation for branch names (optional)
        branch_regex = r"^[a-zA-Z0-9\-_/]+$"
        if not re.match(branch_regex, branch):
            raise ValueError(f"Invalid branch name at index {index}: '{branch}' contains invalid characters.")

# Example usage
json_input = '''
{
  "repositories": [
    {
      "name": "repo1",
      "branch": "main"
    },
    {
      "name": "repo2",
      "branch": "develop"
    },
    {
      "name": "repo3",
      "branch": "feature/new-feature"
    }
  ]
}
'''

# To test invalid cases, replace the json_input with invalid structures as before

validator = JSONValidator(json_input)

# Validate the JSON
try:
    valid_data = validator.validate_json()
    print("JSON is valid and well-formed:", valid_data)
except ValueError as e:
    print(e)



import json

class JSONValidator:
    def __init__(self, json_input):
        self.json_input = json_input
        self.data = None

    # Function to load the JSON
    def load_json(self):
        try:
            self.data = json.loads(self.json_input)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")

    # Function to validate the top-level structure and repositories
    def validate_json(self):
        self.load_json()

        repositories = self.data.get('repositories', None)
        if not isinstance(repositories, list) or len(repositories) == 0:
            raise ValueError("Invalid JSON structure: 'repositories' field is missing or not a non-empty list.")

        # Loop through repositories and validate them
        for index, repo in enumerate(repositories):
            self.validate_repository(repo, index)

        return self.data

    # Function to validate each repository entry
    def validate_repository(self, repo, index):
        if not isinstance(repo, dict):
            raise ValueError(f"Invalid repository entry at index {index}: Each repository must be an object. Found: {type(repo)}")

        if 'name' not in repo or 'branch' not in repo:
            raise ValueError(f"Invalid repository structure at index {index}: Each repository must have 'name' and 'branch' fields. Invalid repository: {repo}")

        # Strip once and validate
        name = repo['name'].strip()
        branch = repo['branch'].strip()

        if not name:
            raise ValueError(f"Invalid repository name at index {index}: Repository 'name' must be a non-empty string. Invalid value: {repo['name']}")

        if not branch:
            raise ValueError(f"Invalid branch name at index {index}: Repository 'branch' must be a non-empty string. Invalid value: {repo['branch']}")


# Example usage
json_input = '''
{
  "repositories": [
    {
      "name": "repo1",
      "branch": "main"
    },
    {
      "name": "repo2",
      "branch": "develop"
    },
    {
      "name": "repo3",
      "branch": "feature/new-feature"
    }
  ]
}
'''

# To test invalid cases, replace the json_input with invalid structures as before

validator = JSONValidator(json_input)

# Validate the JSON
try:
    valid_data = validator.validate_json()
    print("JSON is valid and well-formed:", valid_data)
except ValueError as e:
    print(e)





import json

# Function to validate and read the JSON input
def validate_and_read_json(json_input):
    try:
        # Try to load the JSON input
        data = json.loads(json_input)

        # Perform validation on the structure
        if 'repositories' not in data or not isinstance(data['repositories'], list):
            raise ValueError("Invalid JSON structure: 'repositories' field is missing or not a list.")

        if len(data['repositories']) == 0:
            raise ValueError("Invalid JSON: 'repositories' list cannot be empty.")

        for index, repo in enumerate(data['repositories']):
            # Check if 'name' and 'branch' fields exist
            if not isinstance(repo, dict):
                raise ValueError(f"Invalid repository entry at index {index}: Each repository must be an object. Found: {type(repo)}")

            if 'name' not in repo or 'branch' not in repo:
                raise ValueError(f"Invalid repository structure at index {index}: Each repository must have 'name' and 'branch' fields. Invalid repository: {repo}")

            # Check if 'name' and 'branch' are non-empty strings
            if not isinstance(repo['name'], str) or not repo['name'].strip():
                raise ValueError(f"Invalid repository name at index {index}: Repository 'name' must be a non-empty string. Invalid value: {repo['name']}")

            if not isinstance(repo['branch'], str) or not repo['branch'].strip():
                raise ValueError(f"Invalid branch name at index {index}: Repository 'branch' must be a non-empty string. Invalid value: {repo['branch']}")

        return data

    except json.JSONDecodeError as e:
        # Raise an exception if the JSON is not valid
        raise ValueError(f"Invalid JSON format: {str(e)}")

# Example usage (switch between valid/invalid JSON to test)

# Example valid JSON input
json_input = '''
{
  "repositories": [
    {
      "name": "repo1",
      "branch": "main"
    },
    {
      "name": "repo2",
      "branch": "develop"
    },
    {
      "name": "repo3",
      "branch": "feature/new-feature"
    }
  ]
}
'''

# Example invalid JSON input with missing branch (uncomment to test)
# json_input = '''
# {
#   "repositories": [
#     {
#       "name": "repo1"
#     }
#   ]
# }
# '''

# Example invalid JSON input with empty name and branch (uncomment to test)
# json_input = '''
# {
#   "repositories": [
#     {
#       "name": "",
#       "branch": "main"
#     },
#     {
#       "name": "repo2",
#       "branch": ""
#     }
#   ]
# }
# '''

# Example invalid JSON input with non-string fields (uncomment to test)
# json_input = '''
# {
#   "repositories": [
#     {
#       "name": 123,
#       "branch": "main"
#     }
#   ]
# }
# '''

# Example invalid JSON input with empty repositories (uncomment to test)
# json_input = '''
# {
#   "repositories": []
# }
# '''

# Validate the JSON
try:
    data = validate_and_read_json(json_input)
    print("JSON is valid and well-formed:", data)
except ValueError as e:
    print(e)
