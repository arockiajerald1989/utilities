import re
import json
from pathlib import Path
from datetime import datetime

def extract_last_dict_between_timestamps(file_path, start_timestamp, end_timestamp):
    """
    Extract the last valid JSON dictionary between two timestamps from a single log file.
    Handles both single-line and multiline JSON dictionaries.
    
    Args:
        file_path (str): Path to the log file
        start_timestamp (str): Start time in 'YYYY-MM-DD HH:MM:SS' format
        end_timestamp (str): End time in 'YYYY-MM-DD HH:MM:SS' format
    
    Returns:
        dict: Last valid JSON dictionary found within the time range, or None if none found
    
    Raises:
        ValueError: If timestamps are not in the correct format
        FileNotFoundError: If the specified file does not exist
    """
    # Validate timestamp format
    try:
        datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')
        datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Timestamps must be in 'YYYY-MM-DD HH:MM:SS' format")

    # Check if file exists
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Regex pattern for timestamp
    timestamp_pattern = re.compile(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]')

    last_dict = None
    json_buffer = ""
    current_timestamp = None

    # Process file line-by-line
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            timestamp_match = timestamp_pattern.match(line)
            
            if timestamp_match:
                # New timestamp found, process any buffered JSON
                if json_buffer:
                    try:
                        parsed_dict = json.loads(json_buffer)
                        if (current_timestamp and 
                            start_timestamp <= current_timestamp <= end_timestamp):
                            last_dict = parsed_dict
                    except json.JSONDecodeError:
                        pass  # Reset buffer if invalid JSON
                    json_buffer = ""
                
                # Set new current timestamp
                current_timestamp = line[1:20]  # 'YYYY-MM-DD HH:MM:SS'
                # Start buffering from the rest of the line after timestamp
                json_buffer = line[21:].strip()
            elif current_timestamp:
                # Continue buffering if we have an active timestamp
                json_buffer += " " + line

    # Process any remaining buffered JSON after file ends
    if json_buffer:
        try:
            parsed_dict = json.loads(json_buffer)
            if (current_timestamp and 
                start_timestamp <= current_timestamp <= end_timestamp):
                last_dict = parsed_dict
        except json.JSONDecodeError:
            pass

    return last_dict

# Example usage
if __name__ == "__main__":
    file_path = "log_file.txt"
    start_time = "2025-01-01 11:00:00"
    end_time = "2025-01-01 12:00:00"

    try:
        result = extract_last_dict_between_timestamps(file_path, start_time, end_time)
        print(f"File: {file_path}")
        print(f"Last Extracted Dictionary: {result}")
    except Exception as e:
        print(f"File: {file_path}")
        print(f"Error: {str(e)}")
