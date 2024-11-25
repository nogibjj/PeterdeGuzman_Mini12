"""
Extract and Transform Functions
"""

import requests
import gzip
import json
import csv

import requests
import gzip
import json
import csv


# extract function that downloads and unzips json.gz file from link


# Transform to CSV
import json
import csv


def parse_json_to_csv(input_json_file, output_csv_file="output.csv"):
    """
    Parse a JSON file and save its contents into a CSV file.

    :param input_json_file: Path to the input JSON file (can contain a list of objects).
    :param output_csv_file: Name of the output CSV file (default is 'output.csv').
    """
    try:
        # Step 1: Open and load the JSON data
        with open(input_json_file, "r", encoding="utf-8") as f:
            data = []
            for line in f:
                try:
                    # Attempt to load each line as a separate JSON object
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Skipping line due to error: {e}")

        # Check if the data is a list of records
        if not data or not isinstance(data, list):
            print("No valid data found or unexpected format.")
            return

        # Step 2: Extract headers (keys) from the first item
        headers = data[0].keys() if data else []

        # Step 3: Write to CSV
        with open(output_csv_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            # Write each item (row) in the JSON as a CSV row
            for row in data:
                writer.writerow(row)

        print(f"CSV file '{output_csv_file}' has been created successfully.")

    except Exception as e:
        print(f"Error processing the JSON file: {e}")


# Example usage
if __name__ == "__main__":
    input_json_file = "/Users/pdeguz01/Documents/git/PeterdeGuzman_Mini12/goodreads_book_authors.json"  # Replace with your JSON file path
    parse_json_to_csv(input_json_file)
