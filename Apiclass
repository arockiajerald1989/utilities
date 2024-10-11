import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class TaskAPI:
    def __init__(self, task_id, base_url):
        self.task_id = task_id
        self.base_url = base_url
        self.token = os.getenv('API_TOKEN')  # Get the token from the environment variable

    def _make_request(self, endpoint, method="GET", data=None):
        url = f"{self.base_url}/{endpoint}/{self.task_id}"
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data)
            else:
                raise ValueError("Unsupported HTTP method.")
            
            response.raise_for_status()  # Raises an error for bad status codes (4xx, 5xx)
            return response.json()  # Return response in JSON format
        except requests.exceptions.RequestException as e:
            print(f"Error in API call: {e}")
            return None

    def roll_call(self):
        """Check the current status of the task by making a roll call."""
        data = {"jobstate": "Pending"}
        print(f"Calling Roll Call for Task {self.task_id} with jobstate: Pending")
        return self._make_request("roll_call", method="GET", data=data)

    def stop(self):
        """Stop the task."""
        data = {"jobstate": "Stopped"}
        print(f"Stopping Task {self.task_id} with jobstate: Stopped")
        return self._make_request("stop", method="PUT", data=data)

    def cancel(self):
        """Cancel the task."""
        data = {"jobstate": "Cancelled"}
        print(f"Cancelling Task {self.task_id} with jobstate: Cancelled")
        return self._make_request("cancelled", method="PUT", data=data)

# Example usage:
# Ensure that the .env file is correctly loaded and the token is available
# task_api = TaskAPI("12345", "https://api.example.com/tasks")
# task_api.roll_call()
# task_api.stop()
# task_api.cancel()
