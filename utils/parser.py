import pandas as pd
import re
from datetime import datetime

def parse_log(file_path):
    """
    Parses a log file and extracts timestamp and IP address from each line.
    Returns a pandas DataFrame.
    """

    # Open and read the log file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Example log format:
    # [2025-07-04 12:34:56] ERROR: Failed login from 192.168.1.101
    pattern = re.compile(r'\[(.*?)\].*?from (\d+\.\d+\.\d+\.\d+)')

    # Store parsed results
    data = []

    for line in lines:
        match = pattern.search(line)
        if match:
            try:
                timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                ip = match.group(2)
                data.append({'timestamp': timestamp, 'ip': ip})
            except Exception as e:
                print(f"Skipping line due to error: {e}")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    return df
