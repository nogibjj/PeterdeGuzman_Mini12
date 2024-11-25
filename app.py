from flask import Flask, jsonify, request, render_template
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Initialize the DynamoDB resource with LocalStack endpoint
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",  # LocalStack DynamoDB endpoint
    aws_access_key_id="fakeMyKeyId",  # Dummy credentials
    aws_secret_access_key="fakeSecretAccessKey",
)

# Reference the DynamoDB table
table = dynamodb.Table("Authors")


# Create the Flask home page
@app.route("/")
def home():
    return render_template("homepage.html")


from flask import Flask, jsonify, request, render_template
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# Initialize the DynamoDB resource with LocalStack endpoint
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:4566",  # LocalStack DynamoDB endpoint
    aws_access_key_id="fakeMyKeyId",  # Dummy credentials
    aws_secret_access_key="fakeSecretAccessKey",
)

# Reference the DynamoDB table
table = dynamodb.Table("Authors")


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/authors", methods=["GET"])
def get_author_average_rating():
    # Get the 'name' parameter from the request
    author_name = request.args.get("name")

    if not author_name:
        return jsonify({"error": "Please provide an author name"}), 400

    try:
        # Query DynamoDB table using the Global Secondary Index (GSI) by 'name'
        response = table.query(
            IndexName="NameIndex",  # Use the GSI
            KeyConditionExpression=boto3.dynamodb.conditions.Key("name").eq(
                author_name
            ),
        )

        # Get the items (books) from the response
        items = response.get("Items", [])

        if not items:
            return jsonify({"message": f"No books found for author {author_name}"}), 404

        # Extract the average rating from the first item (assuming the author has only one entry)
        author_item = items[0]

        if "average_rating" not in author_item:
            return (
                jsonify(
                    {"message": f"No average rating found for author {author_name}"}
                ),
                404,
            )

        # Extract the average rating and prepare the result
        avg_rating = author_item["average_rating"]

        # Render the result in an HTML template
        return render_template(
            "results.html", author=author_name, average_rating=avg_rating
        )

    except NoCredentialsError:
        return jsonify({"error": "No valid credentials found for DynamoDB"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)
