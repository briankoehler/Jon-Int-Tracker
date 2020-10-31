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

    # Initialization
    summoners = []

    # Retrieving summoner info from pickle
    pickle_file = open('summoners.pkl', 'rb')
    number_of_sums = pickle.load(pickle_file)
    summoners_list = pickle.load(pickle_file)

    # Adding Summoner objects to list
    for i in range(number_of_sums):
        newSum = Summoner(i, summoners_list[i].name, summoners_list[i].encrypted_id, summoners_list[i].last_game_id)
        log(f'Summoner {newSum.name} found in pickle...')
        summoners.append(newSum)

    for summoner in summoners:

        log(f'Checking {summoner.name}...')

        # API Call
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summoner.encrypted_id + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
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
            log('Got most recent match...')
        except:
            log('Error getting match info...')
            continue

        # Check if a Summoner's Rift
        if rm.queue != 400 and rm.queue != 420 and rm.queue != 440 and rm.queue != 700: # Draft, Solo, Flex, Clash
            log('Match was not on Rift - Ignoring...')
            continue

        # Make sure not an old game
        LAST_GAME = summoner.last_game_id
        if str(rm.game_id) != str(LAST_GAME):
            summoners[summoner.id].last_game_id = rm.game_id
            log('Match is a new match...')
        else:
            log('Old Match - Ignoring...')
            continue

        # Second API Call to check game stats
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matches/' + str(rm.game_id) + '?&api_key=' + RIOT_KEY)
        match_summary = json.loads(response.text)

        # Determine which participant is the current summoner and assign info
        summoner_stats_info = None
        parts = match_summary['participants']
        for p in parts:
            if p['championId'] == rm.champion and p['timeline']['role'] == rm.role and p['timeline']['lane'] == rm.lane:
                summoner_stats_info = p

        # Grab info we want from stats
        kills = summoner_stats_info['stats']['kills']
        deaths = summoner_stats_info['stats']['deaths']

        # Sending a Discord message
        if deaths - kills >= int(DIFF):
            log('Sending a Discord message...')
            channel = client.get_channel(int(CHANNEL)) # TODO Change this to be more flexible
            if deaths > 19:
                await channel.send(f'**{str(deaths)} deaths** this game for {summoner.name}?  Could he get banned??')
                continue
            if deaths > 10:
                await channel.send(f'{summoner.name} just had a **TURBO** int with **{str(deaths)} deaths!** Could he get banned for this??')
                continue
            await channel.send(f'{summoner.name} just died **{str(deaths)} times!** Wow!')
            continue
        log('Kill-Death difference was not large enough - Ignoring...')


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
