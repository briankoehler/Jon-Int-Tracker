# init.py
import requests, json

print('Thank you for using Jon Int Tracker (JIT).')
DISCORD_TOKEN = input('Enter your Discord API token: ')
DISCORD_GUILD = input('Enter your Discord Guild Name: ')
RIOT_KEY = input('Enter your Riot API key: ')
DIFF = input('Enter necessary kill-death difference: ')

# API Call
response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/aAX05Uf5lrObicds4lcyq7El4rOGJyPUUxu2vu7_5wqoog?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
most_recent_match = json.loads(response.text)
game_id = most_recent_match['matches'][0]['gameId']

with open('.env', 'w') as file:
    file.write('# .env\n\n')
    file.write('# Discord Variables\n')
    file.write('DISCORD_TOKEN = ' + DISCORD_TOKEN + '\n')
    file.write('DISCORD_GUILD = ' + DISCORD_GUILD+ '\n')
    file.write('\n')
    file.write('# Riot Variables\n')
    file.write('RIOT_KEY = ' + RIOT_KEY+ '\n')
    file.write('ACCOUNT_NO = aAX05Uf5lrObicds4lcyq7El4rOGJyPUUxu2vu7_5wqoog\n')
    file.write('LAST_GAME = ' + str(game_id)+ '\n')
    file.write('\n')
    file.write('# App Variables\n')
    file.write('DIFF = ' + DIFF + '\n')