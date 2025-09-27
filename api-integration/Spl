import requests
import json

class SplunkHECPlugin:
    """
    A plugin to post JSON data to Splunk using the HTTP Event Collector (HEC) API.

    This class is designed to facilitate easy integration with Splunk by providing
    methods to send JSON data, either directly or from a file, to the Splunk HEC endpoint.
    """

    def __init__(self, hec_url, hec_token):
        """
        Initializes the SplunkHECPlugin with the necessary HEC endpoint details.

        Parameters:
            hec_url (str): The URL of the Splunk HEC endpoint.
            hec_token (str): The authentication token for the Splunk HEC.
        """
        self.hec_url = hec_url
        self.hec_token = hec_token
        self.headers = {
            "Authorization": f"Splunk {self.hec_token}",
            "Content-Type": "application/json"
        }

    def post_json_from_file(self, file_path):
        """
        Reads JSON data from a file and posts it to Splunk HEC.

        Parameters:
            file_path (str): The path to the JSON file to be sent to Splunk.

        Returns:
            None

        Raises:
            IOError: If the file cannot be read.
            json.JSONDecodeError: If the file does not contain valid JSON data.
        """
        try:
            with open(file_path, "r") as file:
                json_data = json.load(file)
            return self.post_json(json_data)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Failed to read JSON data from file. Error: {e}")

    def post_json(self, json_data):
        """
        Posts JSON data directly to the Splunk HEC endpoint.

        Parameters:
            json_data (dict): A dictionary containing the JSON data to be sent.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: For network-related errors when posting data.
        """
        payload = {
            "event": json_data,
            "sourcetype": "_json"
        }
        
        try:
            response = requests.post(self.hec_url, headers=self.headers, data=json.dumps(payload), verify=False)
            if response.status_code == 200:
                print("Data posted successfully to Splunk.")
            else:
                print(f"Failed to post data to Splunk. Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Define the HEC URL and token for Splunk
    hec_url = "https://your-splunk-server:8088/services/collector/event"  # Replace with your Splunk HEC URL
    hec_token = "your-hec-token"  # Replace with your Splunk HEC token
    
    # Define the path to the JSON file to be posted
    file_path = "data.json"  # Replace with your JSON file path

    # Initialize the SplunkHECPlugin instance and post data
    splunk_plugin = SplunkHECPlugin(hec_url, hec_token)
    splunk_plugin.post_json_from_file(file_path)
