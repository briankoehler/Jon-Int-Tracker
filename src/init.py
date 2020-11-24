# init.py
import requests, json
import pickle
import time
from datetime import date
from summoners import Summoner
from leaderboard import Match
from bot import Game

response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
champions = json.loads(response.text)


def main():
    summoners_names_list = []
    summoners_list = []

    # Int Updates
    print('Thank you for using Jon Int Tracker (JIT).\nAnswers to the following questions will be to track inting of a user.')
    DISCORD_TOKEN = input('Enter your Discord API token: ')
    DISCORD_CHANNEL = input('Enter your Discord Channel ID: ')
    RIOT_KEY = input('Enter your Riot API key: ')
    DIFF = input('Enter necessary kill-death difference: ')

    # Writing .env file
    with open('.env', 'w') as file:
        file.write('# .env\n\n')
        file.write('# Discord Variables\n')
        file.write(f'DISCORD_TOKEN="{DISCORD_TOKEN}"\n')
        file.write(f'DISCORD_CHANNEL="{DISCORD_CHANNEL}"\n')
        file.write('\n')
        file.write('# Riot Variables\n')
        file.write(f'RIOT_KEY="{RIOT_KEY}"\n')
        file.write('\n')
        file.write('# App Variables\n')
        file.write(f'DIFF="{DIFF}"\n')

    # Initializing leaderboard file
    matches = []
    for i in range(10):
        new_match = Match(1, '', -1, -1, -1)
        matches.append(new_match)

    # Leaderboard Creation
    with open('leaderboard.pkl', 'wb') as output:
        pickle.dump(matches, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()