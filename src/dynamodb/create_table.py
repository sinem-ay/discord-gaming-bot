import boto3


dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName="games",
    KeySchema=[{"AttributeName": "game_name", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "game_name", "AttributeType": "S"}],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

table.wait_until_exists()
print(f"Table created successfully")
