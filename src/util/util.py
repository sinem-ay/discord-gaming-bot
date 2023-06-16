import os
import random
import requests
from typing import List


EPIC_GAMES_API = os.environ["EPIC_GAMES_API"]
STEAMSPY_API = os.environ["STEAMSPY_API"]


def team_generator(users: List[str]) -> List[str]:
    teams = len(users) // 2
    random.shuffle(users)
    team_1, team_2 = users[:teams], users[teams:]
    return team_1, team_2


def get_free_games() -> List[dict]:
    response = requests.get(EPIC_GAMES_API)
    data = response.json()
    games = data["data"]["Catalog"]["searchStore"]["elements"]

    games_list = []
    for game in games:
        game_url = (
            f"https://www.epicgames.com/store/en-US/product/{game['productSlug']}"
        )
        games_list.append(
            {
                "title": game["title"],
                "url": game_url,
                "image": game["keyImages"][0]["url"],
            }
        )

    return games_list


def get_game_details() -> List[dict]:
    try:
        response = requests.get(STEAMSPY_API)
        data = response.json()

        game_details = []
        for game_id, game_info in data.items():
            game_name = game_info["name"]
            developer = game_info["developer"]
            game_dict = {
                "game_name": game_name,
                "developer": developer,
                "rating_discord": 0,
            }
            game_details.append(game_dict)

        return game_details

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching data: {e}")
