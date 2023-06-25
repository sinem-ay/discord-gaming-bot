import os
import random
import requests
from datetime import datetime
from typing import List, Tuple


EPIC_GAMES_API = os.environ["EPIC_GAMES_API"]
STEAMSPY_API = os.environ["STEAMSPY_API"]


def team_generator(users: List[str], teams: int) -> List[str]:
    random.shuffle(users)
    team_list = []
    start_index = 0
    users_per_team = len(users) // teams
    remaining_users = len(users) % teams

    for i in range(teams):
        if remaining_users > 0:
            num_users = users_per_team + 1
            remaining_users -= 1
        else:
            num_users = users_per_team

        end_index = start_index + num_users
        team_users = users[start_index:end_index]

        teams_dict = {"team_number": f"Team {i+1}", "users": team_users}
        team_list.append(teams_dict)
        start_index = end_index

    return team_list


def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def add_games_list(game: dict, game_url: str, game_list: list) -> None:
    game_list.append(
        {
            "title": game["title"],
            "url": game_url,
            "image": game["keyImages"][0]["url"],
        }
    )


def get_free_games() -> Tuple[List[dict], List[dict]]:
    response = requests.get(EPIC_GAMES_API)
    data = response.json()
    games = data["data"]["Catalog"]["searchStore"]["elements"]

    free_games, upcoming_free_games = [], []
    for game in games:
        promotions = game["promotions"]
        if promotions:
            offers = (
                promotions["upcomingPromotionalOffers"]
                or promotions["promotionalOffers"]
            )
            offer = offers[0]["promotionalOffers"][0]
            start_date, end_date = offer["startDate"], offer["endDate"]
            game_url = (
                f"https://www.epicgames.com/store/en-US/product/{game['productSlug']}"
            )
            current_date = datetime_to_string(datetime.now())
            if start_date <= current_date and end_date > current_date:
                add_games_list(game, game_url, free_games)
            if start_date > current_date:
                add_games_list(game, game_url, upcoming_free_games)

    return free_games, upcoming_free_games


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
