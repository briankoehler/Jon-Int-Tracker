# bot.py
import os
import discord
import requests, json
import pickle
import datetime
import dotenv
from dotenv import load_dotenv
from init import Summoner
from discord.ext import tasks, commands

# Loading Environemnt Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
RIOT_KEY = os.getenv('RIOT_KEY')
ACCOUNT_NO = os.getenv('ACCOUNT_NO')
DIFF = os.getenv('DIFF')


# Bot Client
client = commands.Bot(command_prefix = '!')


# Game Class
class Game:
    def __init__(self, game_id, champion, role, lane, queue):
        self.game_id = game_id
        self.champion = champion
        self.role = role
        self.lane = lane
        self.queue = queue


def log(message):
    print(f'[{datetime.datetime.now()}] {message}')


@tasks.loop(seconds=10)
async def get_int():
    log('Executing get_int task...')

    # API Call
    response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + ACCOUNT_NO + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
    most_recent_match = json.loads(response.text)

    # Storing information
    try:
        rm = Game(
            most_recent_match['matches'][0]['gameId'], 
            most_recent_match['matches'][0]['champion'], 
            most_recent_match['matches'][0]['role'],
            most_recent_match['matches'][0]['lane'],
            most_recent_match['matches'][0]['queue']
        )
    except:
        log('Error getting match info...')
        return

    # Check if a Summoner's Rift
    if rm.queue != 400 and rm.queue != 420 and rm.queue != 440 and rm.queue != 700: # Draft, Solo, Flex, Clash
        return

    # Make sure not an old game
    LAST_GAME = os.getenv('LAST_GAME')
    log('LAST_GAME: ' + LAST_GAME)
    if str(rm.game_id) != LAST_GAME:
        os.environ['LAST_GAME'] = str(rm.game_id)
        dotenv_file = dotenv.find_dotenv()
        dotenv.set_key(dotenv_file, 'LAST_GAME', os.environ['LAST_GAME'])
        log('Found a new completed match...')
    else:
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
        log('Sending a Discord message...')
        channel = client.get_channel(int(CHANNEL)) # TODO Change this to be more flexible
        if deaths > 19:
            await channel.send('**' + str(deaths) + ' deaths** this game for Jon?  Could he get banned??')
            return
        if deaths > 15:
            await channel.send('Jon just had a **TURBO** int with **' + str(deaths) + ' deaths!** Could he get banned for this??')
            return
        await channel.send('Jon just died **' + str(deaths) + ' times!** Wow!')
        return
    log('Kill-Death difference not large enough...')

# WIP
@tasks.loop(seconds=10)
async def update_leaderboard():
    log('Updating leaderboard...')

    with open('../leaderboard_summoners.pkl', 'rb') as input:
        number_of_sums = pickle.load(input)
        summoners = pickle.load(input)
        for summoner in summoners:
            log('ned')

# After deploying...
@client.event
async def on_ready():
    log(f'{client.user.name} has connected to Discord!')
    get_int.start()


# Reacting to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!jit':
        response = '**ned** test'
        await message.channel.send(response)

    if message.content == '!leaderboard':
        response = 'Leaderboard goes here'
        await message.channel.send(response)


client.run(TOKEN)
