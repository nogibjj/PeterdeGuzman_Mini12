"""
Transform and Load Functions
"""

import boto3
from botocore.exceptions import ClientError


def create_table():
    # Connecting to LocalStack DynamoDB instance
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")

    # Create Table
    try:
        table = dynamodb.create_table(
            TableName="Books",
            KeySchema=[
                {"AttributeName": "author_name", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "book_title", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "author_name", "AttributeType": "S"},
                {"AttributeName": "book_title", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Books")
        print(f"Table '{table.name}' created.")
    except ClientError as e:
        print(f"Error creating table: {e}")
