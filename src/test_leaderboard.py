import pickle
import requests, json
from init import Summoner, Match, Game
from datetime import date

response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
champions = json.loads(response.text)

matches = []

match_1 = Match(17, "The Mindwalker", 4, 30, 0)
matches.append(match_1)
match_2 = Match(17, "The Mindwalker", 4, 26, 0)
matches.append(match_2)
match_3 = Match(17, "The Mindwalker", 4, 25, 0)
matches.append(match_3)
match_4 = Match(17, "The Mindwalker", 4, 24, 0)
matches.append(match_4)
match_5 = Match(17, "The Mindwalker", 4, 23, 0)
matches.append(match_5)
match_6 = Match(17, "The Mindwalker", 4, 22, 0)
matches.append(match_6)
match_7 = Match(17, "The Mindwalker", 4, 21, 0)
matches.append(match_7)
match_8 = Match(17, "The Mindwalker", 4, 20, 0)
matches.append(match_8)
match_9 = Match(17, "The Mindwalker", 4, 19, 0)
matches.append(match_9)
match_10 = Match(17, "The Mindwalker", 4, 18, 0)
matches.append(match_10)

with open('leaderboard.pkl', 'wb') as output:
    pickle.dump(matches, output, pickle.HIGHEST_PROTOCOL)