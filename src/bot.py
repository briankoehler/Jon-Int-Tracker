# bot.py
import os, datetime, pickle
import discord
import requests, json
import dotenv
from init import Summoner, Game, Match
from leaderboard import *
from dotenv import load_dotenv
from discord.ext import tasks, commands
from datetime import date

# Loading Environemnt Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = os.getenv('DISCORD_CHANNEL')
RIOT_KEY = os.getenv('RIOT_KEY')
DIFF = os.getenv('DIFF')

# Loading Champions based on ID
response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
champions = json.loads(response.text)


# Bot Client
bot = commands.Bot(command_prefix = '?')


def log(message):
    """Prints a message to the console with date/time

    Args:
        message (String): Message to print
    """
    print(f'[{datetime.datetime.now()}] {message}')

def load_summoners():
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        log('Summoners file not found...')
        return
    return pickle.load(pickle_file), pickle.load(pickle_file)

def update_summoners(summoners_list):
    """Updates the summoners pickle

    Args:
        summoners_list (List): List containing summoners to track
    """
    with open('summoners.pkl', 'wb') as output:
        pickle.dump(len(summoners_list), output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(summoners_list, output, pickle.HIGHEST_PROTOCOL)


def is_int(kills, deaths, assists):
    """Determines whether or not a match with given kda is an "int"

    Args:
        kills (int): # of kills
        deaths (int): # of deaths
        assists (int): # of assists

    Returns:
        boolean: True if int, False if not
    """
    return False


@tasks.loop(seconds=10)
async def get_int():
    """Every 10s, check most recent match for every summoner int the summoners pickle and determine if it is an int"""

    log('Executing get_int task...')

    # Initialization
    summoners = []

    # Retrieving summoner info from pickle
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        log('Summoners file not found...')
        return
    number_of_sums = pickle.load(pickle_file)
    summoners_list = pickle.load(pickle_file)

    # Adding Summoner objects to list
    for i in range(number_of_sums):
        newSum = Summoner(i, summoners_list[i].name, summoners_list[i].encrypted_id, summoners_list[i].last_game_id)
        # log(f'Summoner {newSum.name} found in pickle...')
        summoners.append(newSum)

    for summoner in summoners:

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
            if rm.lane == 'MID':
                rm.lane = 'MIDDLE'
        except:
            log(f'Error getting match info for {summoner.name}...')
            continue

        # Check if a Summoner's Rift
        if rm.queue != 400 and rm.queue != 420 and rm.queue != 440 and rm.queue != 700: # Draft, Solo, Flex, Clash
            continue

        # Make sure not an old game
        LAST_GAME = summoner.last_game_id
        if str(rm.game_id) != str(LAST_GAME):
            summoners[summoner.id].last_game_id = rm.game_id
        else:
            continue

        # Second API Call to check game stats
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matches/' + str(rm.game_id) + '?&api_key=' + RIOT_KEY)
        match_summary = json.loads(response.text)

        # Determine which participant is the current summoner and assign info
        summoner_stats_info = None
        parts = match_summary['participants']
        for p in parts:
            if str(p['championId']) == str(rm.champion) and str(p['timeline']['role']) == str(rm.role) and str(p['timeline']['lane']) == str(rm.lane):
                summoner_stats_info = p

        # Grab info we want from stats
        kills = summoner_stats_info['stats']['kills']
        deaths = summoner_stats_info['stats']['deaths']
        assists = summoner_stats_info['stats']['assists']

        # Sending a Discord message TODO Add more message variation
        if deaths - kills >= int(DIFF):
            new_leaderboard_match = Match(rm.champion, summoner.name, kills, deaths, assists)
            update_leaderboard(new_leaderboard_match)
            log(f'Sending a Discord message for {summoner.name}...')
            channel = bot.get_channel(int(CHANNEL)) # TODO Change this to be more flexible
            if deaths > 19:
                msg = f'{summoner.name} just had a **TURBO** int with **{str(deaths)} deaths!** Could he get banned for this??'
            elif deaths > 14:
                msg = f'**{str(deaths)} deaths** this game for {summoner.name}? Was he even trying?'
            else:
                msg = f'{summoner.name} just died **{str(deaths)} times!** Wow!'
            await channel.send(msg)

        # Updating Pickle File
        update_summoners(summoners)


# Leaderboard Command
@bot.command()
async def leaderboard(ctx):
    """Sends a message with the top 10 int matches"""

    leaderboard_list = load_leaderboard()
    leaderboard_string = '_ _\n\n**INT LEADERBOARD**\n--------------------\n'
    num = 1
    for match in leaderboard_list:
        leaderboard_string += f'**{num})** {match.kills}/{match.deaths}/{match.assists} - {match.summoner} ({match.champ})\n'
        num = num + 1
    await ctx.send(leaderboard_string)


# List Summoners being tracked
@bot.command()
async def list(ctx):
    """Sends a message with all summoners being tracked"""

    # Initialization
    summoners_string = '_ _\n\n**SUMMONERS BEING TRACKED**\n--------------------\n'

    # Retrieving summoner info from pickle
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        log('Summoners file not found...')
        return
    number_of_sums = pickle.load(pickle_file)
    summoners_list = pickle.load(pickle_file)

    # Adding Summoner names to string of message to send
    for i in range(number_of_sums):
        summoners_string += f'• {summoners_list[i].name} (ID: {summoners_list[i].id})\n'
    await ctx.send(summoners_string)


# Add a new Summoner to keep track of
@bot.command()
async def add(ctx, name):
    """Adds a summoner to the tracking list

    Args:
        name (String): Name of summoner to add
    """

    response = requests.get(url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + RIOT_KEY)
    account_info = json.loads(response.text)
    sumId = account_info['accountId']
    response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + sumId + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
    most_recent_match = json.loads(response.text)
    game_id = most_recent_match['matches'][0]['gameId']

    # Retrieving summoner info from pickle
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        log('Summoners file not found...')
        return
    number_of_sums = pickle.load(pickle_file)
    summoners_list = pickle.load(pickle_file)

    newSum = Summoner(number_of_sums, name, sumId, game_id)
    summoners_list.append(newSum)
    # Dumping list of summoner objects to pickle file
    update_summoners(summoners_list)

    await ctx.send(f'Added **{name}** to tracking list.')


@bot.command()
async def remove(ctx, name):
    """Removes a summoner from traking list

    Args:
        name (String): Name of summoner to remove
    """

    # Retrieving summoner info from pickle
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        log('Summoners file not found...')
        return
    number_of_sums = pickle.load(pickle_file)
    summoners_list = pickle.load(pickle_file)

    found = False
    i = 0
    while i < len(summoners_list):
        if summoners_list[i].name == name:
            found = True
            del summoners_list[i]
            i -= 1
        elif found:
            summoners_list[i].id -= 1
        i += 1

    # Dumping list of summoner objects to pickle file
    update_summoners(summoners_list)

    if found:
        await ctx.send(f'Removed {name} from tracking list.')
        return
    await ctx.send(f'Unable to find {name} in tracking list.')


# After deploying...
@bot.event
async def on_ready():
    log(f'{bot.user.name} has connected to Discord!')
    get_int.start()


bot.run(TOKEN)
