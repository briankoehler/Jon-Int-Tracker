# bot.py
import os, datetime, pickle
import discord
import requests, json
import dotenv
from summoners import load_summoners, update_summoners, Summoner, Game
from leaderboard import update_leaderboard, Match
from discord.ext import tasks, commands
from datetime import date


# Bot Client
bot = commands.Bot(command_prefix = '?')


def log(message):
    """Prints a message to the console with date/time

    Args:
        message (String): Message to print
    """
    print(f'[{datetime.datetime.now()}] {message}')


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
    number_of_sums, summoners_list = load_summoners()

    # Adding Summoner objects to list
    for i in range(number_of_sums):
        
        newSum = Summoner(i, summoners_list[i].name, summoners_list[i].encrypted_id, summoners_list[i].last_game_id)
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


# After deploying...
@bot.event
async def on_ready():
    log(f'{bot.user.name} has connected to Discord!')

    if not os.path.isfile('summoners.pkl'):
        update_summoners([])

    get_int.start()


if __name__ == '__main__':
    # Loading Environemnt Variables
    dotenv.load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL = os.getenv('DISCORD_CHANNEL')
    RIOT_KEY = os.getenv('RIOT_KEY')
    DIFF = os.getenv('DIFF')

    # Loading Champions based on ID
    response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
    champions = json.loads(response.text)

    bot.load_extension("summoners")
    bot.load_extension("leaderboard")

    bot.run(TOKEN)
