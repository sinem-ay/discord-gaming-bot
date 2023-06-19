from typing import List
import boto3
from boto3.dynamodb.conditions import Key, Attr

from util.util import get_game_details

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("games")


def fill_table() -> None:
    items = get_game_details()
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(
                Item={
                    "game_name": item["game_name"],
                    "developer": item["developer"],
                    "rating_discord": item["rating_discord"],
                }
            )
        print("Table filled with game data")


def get_all_games() -> List[dict]:
    response = table.scan()
    data = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])

    return data


def get_game_by_name(game_name: str):
    return table.query(KeyConditionExpression=Key("game_name").eq(f"{game_name}"))


def update_rating_discord(game_name: str, new_rating: int) -> bool:
    response = table.update_item(
        Key={"game_name": game_name},
        UpdateExpression="SET rating_discord = :rating",
        ExpressionAttributeValues={":rating": new_rating},
    )

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return True
    return False


if __name__ == "__main__":
    fill_table()
