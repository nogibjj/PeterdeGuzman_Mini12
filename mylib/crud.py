import csv
import boto3
from botocore.exceptions import ClientError

# Set up session with LocalStack DynamoDB
boto3.setup_default_session(
    aws_access_key_id="fakeMyKeyId",
    aws_secret_access_key="fakeSecretAccessKey",
    region_name="us-east-1",  # Set a valid region
)


import boto3
from botocore.exceptions import ClientError


def create_table(table_name="Authors"):
    """
    Creates a DynamoDB table with 'name' as the partition key.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1",
        endpoint_url="http://localhost:4566",  # LocalStack endpoint
    )

    try:
        # Create the table with `name` as partition key
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "name", "KeyType": "HASH"},  # 'name' as partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "name", "AttributeType": "S"},  # `name` is a string
                {
                    "AttributeName": "author_id",
                    "AttributeType": "S",
                },  # Optional: 'author_id'
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # Wait for the table to be created
        table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        print(f"Table '{table_name}' created successfully.")

    except ClientError as e:
        print(f"Error creating table: {e}")


import csv
import boto3
from botocore.exceptions import ClientError


def load_csv_to_dynamodb(csv_file_path, table_name="Authors"):
    """
    Load data from a CSV file into DynamoDB.

    :param csv_file_path: The path to the CSV file to load.
    :param table_name: The name of the DynamoDB table to insert data into.
    """
    # Connect to DynamoDB (LocalStack in this case)
    dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-east-1",  # Specify a region
        endpoint_url="http://localhost:4566",  # LocalStack endpoint
    )
    table = dynamodb.Table(table_name)

    try:
        # Open the CSV file and read the data
        with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            insert_count = 0  # Counter to track the number of records inserted

            # Iterate over each row in the CSV file
            for row in reader:
                if insert_count >= 500:
                    print("Reached 500 authors. Stopping the insert process.")
                    break

                # Create the item to be inserted into DynamoDB
                item = {
                    "name": row["name"],  # 'name' is the partition key
                    "author_id": row["author_id"],  # Optional: sort key if needed
                    "average_rating": row["average_rating"],
                    "text_reviews_count": row["text_reviews_count"],
                    "ratings_count": row["ratings_count"],
                }

                # Insert the item into DynamoDB
                try:
                    table.put_item(Item=item)
                    insert_count += 1
                    print(
                        f"Inserted item for {row['name']} (author_id: {row['author_id']})"
                    )
                except ClientError as e:
                    print(f"Error inserting item: {e}")

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_table(table_name):
    """
    Delete an existing DynamoDB table.

    :param table_name: The name of the table to delete.
    """
    try:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="us-east-1",  # Specify a region
            endpoint_url="http://localhost:4566",  # LocalStack endpoint
        )
        table = dynamodb.Table(table_name)

        # Deleting the table
        response = table.delete()

        # Wait for the table to be deleted
        table.meta.client.get_waiter("table_not_exists").wait(TableName=table_name)

        print(f"Table '{table_name}' deleted successfully.")
    except ClientError as e:
        print(f"Error deleting table: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def describe_table():
    # Connecting to LocalStack DynamoDB instance
    dynamodb = boto3.client(
        "dynamodb",
        region_name="us-east-1",  # Specify a region
        endpoint_url="http://localhost:4566",  # LocalStack endpoint (or your actual DynamoDB endpoint)
    )

    # Describe the table to check its schema
    try:
        response = dynamodb.describe_table(TableName="Authors")
        print(response)
    except Exception as e:
        print(f"Error describing table: {e}")


# Example usage
if __name__ == "__main__":
    create_table(table_name="Authors")
    csv_file_path = "/Users/pdeguz01/Documents/git/PeterdeGuzman_Mini12/mylib/authors.csv"  # Path to your CSV file
    load_csv_to_dynamodb(csv_file_path)
    describe_table()
