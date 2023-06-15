import os
import random
import requests
from typing import List


EPIC_GAMES_API = os.environ["EPIC_GAMES_API"]


def team_generator(users: List[str]):
    teams = len(users) // 2
    random.shuffle(users)
    team_1, team_2 = users[:teams], users[teams:]
    return team_1, team_2


def get_free_games() -> List[str]:
    games_list = []
    response = requests.get(EPIC_GAMES_API)
    data = response.json()
    games = data["data"]["Catalog"]["searchStore"]["elements"]

    for game in games:
        game_url = (
            f"https://www.epicgames.com/store/en-US/product/{game['productSlug']}"
        )
        games_list.append(f"{game['title']}: {game_url}")

    return games_list
