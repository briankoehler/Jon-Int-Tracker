# bot.py
import os, datetime, pickle, random
import discord
import requests, json
import dotenv
from summoners import load_summoners, update_summoners
from leaderboard import update_leaderboard, write_leaderboard
from class_def import Game, Summoner, Match
from discord.ext import tasks, commands
from datetime import date

# ?s? = Summoner name
# ?S? = All caps Summoner name
# ?d? = # of deaths
# ?k? = # of kills
# ?a? = # of assists
int_messages = {
    'standard': [ # 0-10
        '?s? just died **?d? times!** Wow!',
        '**?k?/?d?/?a?** game coming from ?s?.  Nice.',
        'Oof, **?k?/?d?/?a?** by ?s?. What OP score would that even be??',
        'What a game by ?s?! **?d? deaths and ?k? kills!**',
        'Yikes, **?d? deaths** and only ?k? kills for ?s? that last match.'
    ],
    'heavy': [ # 10-14
        '**NEWS FLASH:** ?S? DROPS A **?d? DEATH** GAME',
        'Damn, ?s? really died **?d? times** in one game.',
        'WOW!  **?d? deaths** by ?s? in this int-heavy game!',
        'Holy moly - **?d? DEATHS** BY ?S?!!'
    ],
    'turbo': [ # 15-19
        'Get **shit** on ?s?! Suck my dick! **?d?**',
        '**BREAKING NEWS:** ?S? INTS ANOTHER GAME WITH **?d? DEATHS**',
        '**HOLY SMOKES!** ?s? just gifted us **?d? deaths!**'
    ],
    'turbo-mega': [ # 20+
        'Incredible.  Once in a blue moon.  A **?d? death* game by ?s?.  We all all honored, ?s?.'
    ]
}


# Bot Client
bot = commands.Bot(command_prefix = '??')


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
    if deaths == 0:
        return False
    
    if ((kills * 2) + assists) / (deaths * 2) < 1.3 and deaths - kills > 2 and deaths > 3:
        if deaths < 6 and kills + assists > 3:
            return False
        if deaths < 10 and kills > 2 and kills + assists > 7:
            return False
        return True
    return False


@tasks.loop(seconds=20)
async def get_int():
    """Every 20s, check most recent match for every summoner int the summoners pickle and determine if it is an int"""

    log('Executing get_int task...')

    # Initialization
    summoners = []

    # Retrieving summoner info from pickle
    number_of_sums, summoners = load_summoners()

    # Checking each summoner's recent game
    for i, summoner in enumerate(summoners):

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
            summoners[i].last_game_id = rm.game_id
        else:
            continue
        
        log(f'Found new game for {summoner.name}')

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
        
        # Updating leaderboard if necessary
        new_leaderboard_match = Match(rm.game_id, rm.champion, summoner.name, kills, deaths, assists)
        update_index = update_leaderboard(new_leaderboard_match)
        
        # Gettinc channel to message
        if CHANNEL == '':
            return
        channel = bot.get_channel(int(CHANNEL)) # TODO Change this to be more flexible

        # Sending a Discord message based on number of deaths
        if is_int(kills, deaths, assists):
            log(f'Sending a Discord message for {summoner.name}...')
            if deaths >= 20:
                msg = random.choice(int_messages['turbo-mega'])
            elif deaths >= 15:
                msg = random.choice(int_messages['turbo'])
            elif deaths >= 10:
                msg = random.choice(int_messages['heavy'])
            else:
                msg = random.choice(int_messages['standard'])
                
            # Replacing variables in template
            msg = msg.replace('?s?', summoner.name)
            msg = msg.replace('?S?', summoner.name.upper())
            msg = msg.replace('?d?', str(deaths))
            msg = msg.replace('?k?', str(kills))
            msg = msg.replace('?a?', str(assists))
            
            await channel.send(msg)
            
            # Sending leaderboard message if necessary
            if update_index != 0:
                await channel.send(f'This is now **#{update_index}** on the int leaderboard!')

        # Updating Pickle File
        update_summoners(summoners)


@bot.command()
async def here(ctx):
    """Sets the notification channel to where this is sent

    Args:
        ctx (Context): Context of command
    """
    # Getting channel id and name
    new_id = ctx.channel.id
    new_name = ctx.channel.name
    
    # Updating environment variable
    dotenv_file = dotenv.find_dotenv()
    os.environ['DISCORD_CHANNEL'] = str(new_id)
    CHANNEL = CHANNEL = os.getenv('DISCORD_CHANNEL')
    dotenv.set_key(dotenv_file, 'DISCORD_CHANNEL', os.environ['DISCORD_CHANNEL'])
    
    await ctx.send(f'Set the notification channel to {new_name} (ID: {new_id})')


@bot.command()
async def jit(ctx):
    """Sends a short about message and a list of commands

    Args:
        ctx (Context): Context of command
    """
    await ctx.send(f'_ _\n\nThank you for using the Jon-Int-Tracker.  Check the Github here: https://github.com/briankoehler/Jon-Int-Tracker\n\n' \
        '?list - View tracking list\n' \
        '?here - Sets the notification channel to wherever this is sent\n' \
        '?add <Summoner Name> - Add a summoner to the tracking list\n' \
        '?remove <Summoner Name> - Remove a summoner from the tracking list\n' \
        '?leaderboard - Display the Int Leadeboard')


@bot.event
async def on_guild_join(guild):
    """Sends a message to whoever invited the bot

    Args:
        guild (Guild): Guild object of joined guild
    """
    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    await bot_entry[0].user.send('_ _\nThanks for using the Jon-Int-Tracker! Use the ?jit command to get started!\nGithub: https://github.com/briankoehler/Jon-Int-Tracker')


@bot.event
async def on_ready():
    log(f'{bot.user.name} has connected to Discord!')

    get_int.start()


if __name__ == '__main__':
    
    if not os.path.isfile('summoners.pkl'):
        update_summoners([])
        
    if not os.path.isfile('leaderboard.pkl'):
        # Initializing leaderboard file
        matches = []
        for i in range(10):
            matches.append('')

        # Leaderboard Creation
        write_leaderboard(matches)
        
    if not os.path.isfile('.env'):
        # Int Updates
        print('Thank you for using Jon Int Tracker (JIT).\nPlease provide the following details to setup the bot.  You can always change the .env file manually afterwards.')
        DISCORD_TOKEN = input('Enter your Discord bot token: ')
        # DISCORD_CHANNEL = input('Enter your Discord Channel ID: ')
        RIOT_KEY = input('Enter your Riot API key: ')

        # Writing .env file
        with open('.env', 'w') as file:
            file.write('# .env\n\n')
            file.write(f'DISCORD_TOKEN="{DISCORD_TOKEN}"\n')
            file.write(f'DISCORD_CHANNEL=""\n')
            file.write(f'RIOT_KEY="{RIOT_KEY}"\n')
        
    # Loading Environemnt Variables
    dotenv.load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL = os.getenv('DISCORD_CHANNEL')
    RIOT_KEY = os.getenv('RIOT_KEY')

    bot.load_extension("summoners")
    bot.load_extension("leaderboard")

    bot.run(TOKEN)
