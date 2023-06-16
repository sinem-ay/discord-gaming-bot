import boto3
from util.util import get_game_details

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("games")


def fill_table():
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


if __name__ == "__main__":
    fill_table()
