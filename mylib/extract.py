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


# def extract(url, output_csv="goodreads_books.csv"):
#     """
#     Extract data from a gzipped JSON file, parse it, and save it as a CSV.

#     :param url: URL of the gzipped JSON file.
#     :param output_csv: The name of the output CSV file (default is 'goodreads_books.csv').
#     """
#     # Step 1: Download the .json.gz file
#     print("Downloading the .json.gz file...")
#     response = requests.get(url)

#     if response.status_code != 200:
#         print(f"Failed to download file. HTTP status code: {response.status_code}")
#         return

#     with open("goodreads_book_authors.json.gz", "wb") as f:
#         f.write(response.content)

#     print("File downloaded and saved as 'goodreads_book_authors.json.gz'.")

#     # Step 2: Decompress the gzipped JSON file
#     try:
#         with gzip.open("goodreads_book_authors.json.gz", "rt", encoding="utf-8") as f:
#             # Step 3: Parse JSON data
#             data = json.load(f)
#     except Exception as e:
#         print(f"Error decompressing or reading the file: {e}")
#         return

#     print(f"Loaded {len(data)} entries from the JSON file.")

#     # Step 4: Extract the data and save it as CSV
#     try:
#         with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
#             writer = csv.writer(csvfile)

#             # Write header row
#             writer.writerow(["author_name", "book_title"])

#             # Iterate over each entry and write to CSV
#             for entry in data:
#                 author_name = entry.get("author_name", "N/A")
#                 book_title = entry.get("book_title", "N/A")

#                 # Write each book entry
#                 writer.writerow([author_name, book_title])

#         print(f"CSV file '{output_csv}' has been created successfully.")
#     except Exception as e:
#         print(f"Error writing to CSV file: {e}")


# # Example usage of the extract function
# if __name__ == "__main__":
#     url = "https://datarepo.eng.ucsd.edu/mcauley_group/gdrive/goodreads/goodreads_book_authors.json.gz"
#     extract(url)


# Transform to CSV
import json
import csv


def parse_json_to_csv(input_json_file, output_csv_file="output.csv"):
    """
    Parse a JSON file and save its contents into a CSV file.

    :param input_json_file: Path to the input JSON file.
    :param output_csv_file: Name of the output CSV file (default is 'output.csv').
    """
    try:
        # Step 1: Load the JSON data
        with open(input_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if the data is a list of objects (as expected)
        if not isinstance(data, list):
            print("Expected a list of records in the JSON file.")
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
    input_json_file = "/Users/pdeguz01/Documents/git/PeterdeGuzman_Mini12/.data/goodreads_book_authors.json"  # Replace with your JSON file path
    parse_json_to_csv(input_json_file)
