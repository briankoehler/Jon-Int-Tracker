# bot.py
import os
import discord
import requests, json
import time, asyncio
import threading
from dotenv import load_dotenv
from discord.ext import tasks, commands

load_dotenv()
# Environemnt Variables
TOKEN = os.getenv('DISCORD_TOKEN')
RIOT_KEY = os.getenv('RIOT_KEY')
ACCOUNT_NO = os.getenv('ACCOUNT_NO')
DIFF = os.getenv('DIFF')

# Stating Intents
#intents = discord.Intents.default()
#intents.members = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = '!')


# Game Class
class Game:
    def __init__(self, game_id, champion, role, lane, queue):
        self.game_id = game_id
        self.champion = champion
        self.role = role
        self.lane = lane
        self.queue = queue


@tasks.loop(seconds=10)
async def get_int():
    print('test')

    while True:

        # API Call
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + ACCOUNT_NO + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
        most_recent_match = json.loads(response.text)

        # Storing information
        rm = Game(
            most_recent_match['matches'][0]['gameId'], 
            most_recent_match['matches'][0]['champion'], 
            most_recent_match['matches'][0]['role'],
            most_recent_match['matches'][0]['lane'],
            most_recent_match['matches'][0]['queue']
        )

        # Check if a solo/duo game (NEEDS TO BE 420) ?

        # Make sure not an old game
        LAST_GAME = os.getenv('LAST_GAME')
        if str(rm.game_id) != LAST_GAME:
            os.environ['LAST_GAME'] = str(rm.game_id)
            with open('.env', 'r') as file:
                data = file.readlines()
            data[10] = 'LAST_GAME = ' + str(rm.game_id) + '\n' # Dependent on line in file
            with open('.env', 'w') as file:
                file.writelines(data)
            break
        return
    
    # Second API Call to check game stats
    response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matches/' + str(rm.game_id) + '?&api_key=' + RIOT_KEY)
    match_summary = json.loads(response.text)

    # Determine which participant is Jon and assign info
    parts = match_summary['participants']
    for p in parts:
        if p['championId'] == rm.champion and p['timeline']['role'] == rm.role and p['timeline']['lane'] == rm.lane:
            jon_info = p

    # Grab info we want from stats
    kills = jon_info['stats']['kills']
    deaths = jon_info['stats']['deaths']

    if deaths - kills >= int(DIFF):
        channel = client.get_channel(769329381902123011) # TODO Change this to be more flexible
        if deaths > 19:
            await channel.send(str(deaths) + ' deaths this game for Jon?  Temp ban coming up!')
        if deaths > 15:
            await channel.send('Jon just had a TURBO int with ' + str(deaths) + ' deaths! Could he get banned for this??')
        await channel.send('Jon just died ' + str(deaths) + ' times! Wow!')


# After connecting...
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    get_int.start()


# Reacting to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!jit':
        response = 'ned test'
        await message.channel.send(response)


client.run(TOKEN)
