# init.py
import requests, json

print('Thank you for using Jon Int Tracker (JIT).')
DISCORD_TOKEN = input('Enter your Discord API token: ')
DISCORD_CHANNEL = input('Enter your Discord Channel ID: ')
RIOT_KEY = input('Enter your Riot API key: ')
SUMMONER_NAME = input('Enter the desired summoner to track: ')
DIFF = input('Enter necessary kill-death difference: ')

# Getting Encrypted Account ID
response = requests.get(url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + SUMMONER_NAME + '?api_key=' + RIOT_KEY)
account_info = json.loads(response.text)
ACCOUNT_ID = account_info['accountId']

# API Call
response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/aAX05Uf5lrObicds4lcyq7El4rOGJyPUUxu2vu7_5wqoog?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
most_recent_match = json.loads(response.text)
game_id = most_recent_match['matches'][0]['gameId']

with open('.env', 'w') as file:
    file.write('# .env\n\n')
    file.write('# Discord Variables\n')
    file.write(f'DISCORD_TOKEN = {DISCORD_TOKEN}\n')
    file.write(f'DISCORD_CHANNEL = {DISCORD_CHANNEL}\n')
    file.write('\n')
    file.write('# Riot Variables\n')
    file.write(f'RIOT_KEY = {RIOT_KEY}\n')
    file.write(f'ACCOUNT_NO = {ACCOUNT_ID}\n')
    file.write(f'LAST_GAME = {str(game_id)}\n')
    file.write('\n')
    file.write('# App Variables\n')
    file.write(f'DIFF = {DIFF}\n')