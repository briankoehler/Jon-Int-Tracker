import pickle
import request, json
from bot import Match
from init import Summoner
from datetime import date

response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
champions = json.loads(response.text)

matches = []

match_1 = Match(17, 4, 30)
matches.append(match_1)
match_2 = Match(17, 4, 26)
matches.append(match_2)
match_3 = Match(17, 4, 25)
matches.append(match_3)
match_4 = Match(17, 4, 24)
matches.append(match_4)
match_5 = Match(17, 4, 23)
matches.append(match_5)
match_6 = Match(17, 4, 22)
matches.append(match_6)
match_7 = Match(17, 4, 21)
matches.append(match_7)
match_8 = Match(17, 4, 20)
matches.append(match_8)
match_9 = Match(17, 4, 19)
matches.append(match_9)
match_10 = Match(17, 4, 18)
matches.append(match_10)

with open('leaderboard.pkl', 'wb') as output:
    pickle.dump(matches, output, pickle.HIGHEST_PROTOCOL)