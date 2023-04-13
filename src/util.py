import random
from typing import List


def team_generator(users: List[str]):
    teams = len(users) // 2
    random.shuffle(users)
    team_1, team_2 = users[:teams], users[teams:]
    return team_1, team_2
