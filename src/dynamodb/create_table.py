import boto3


dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName="games",
    KeySchema=[
        {"AttributeName": "game_name", "KeyType": "HASH"},
        {"AttributeName": "rating_discord", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "game_name", "AttributeType": "S"},
        {"AttributeName": "rating_discord", "AttributeType": "N"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

table.wait_until_exists()
print(f"Table created successfully")
