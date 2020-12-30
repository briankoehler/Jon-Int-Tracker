# bot.py
import os, random, logging
import discord
import requests, json
import dotenv
import database
from class_def import Summoner, Match
from bs4 import BeautifulSoup
from discord.ext import tasks, commands


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


def get_champ_from_id(id):
    """Obtains a champion name given its ID assigned by Riot.

    Args:
        id (int): Champion's ID

    Returns:
        str: Champion's name
    """
    page = requests.get('https://leagueoflegends.fandom.com/wiki/Patch')
    soup = BeautifulSoup(page.content, 'html.parser')
    
    wikitable = soup.find_all('table', class_='wikitable')
    wikitable = wikitable[0]
    patch = wikitable.find_all('a')
    patch = patch[0]
    patch = patch.text
    patch = patch + '.1'
    
    response = requests.get(url=f'http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json')
    champions = json.loads(response.text)
    
    for champion in champions['data']:
        if champions['data'][champion]['key'] == str(id):
            return champion


@tasks.loop(seconds=20)
async def get_int():
    """Every 20s, check most recent match for every summoner int the summoners pickle and determine if it is an int"""

    logging.info('Executing get_int task')
    
    # Checking each summoner of each guild
    for g in database.get_guilds():

        # Retrieving summoners list from database TODO: do by all guilds
        summoners_tuples = database.get_summoners(g[0])
        
        # Initialization
        summoners = []
        
        # Setting Summoner objects
        for s in summoners_tuples:
            summoners.append(Summoner(s[1], s[2], s[3])) # (id, name, last_match)

        # Checking each summoner's recent game
        for i, summoner in enumerate(summoners):

            # API Call
            response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summoner.id + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
            most_recent_match = json.loads(response.text)

            # Storing information about match
            try:
                match_info = Match(most_recent_match['matches'][0]['gameId'], 
                                summoner.name,
                                get_champ_from_id(most_recent_match['matches'][0]['champion']),
                                most_recent_match['matches'][0]['role'], 
                                'MIDDLE' if most_recent_match['matches'][0]['lane'] == 'MID' else most_recent_match['matches'][0]['lane'], 
                                most_recent_match['matches'][0]['queue'])

            except:
                logging.error(f'Error getting match info for {summoner.name}...')
                continue

            # Check if a Summoner's Rift
            if match_info.queue not in set((400, 420, 440, 700)): # Draft, Solo, Flex, Clash
                continue

            # Make sure not an old game
            LAST_MATCH = summoner.last_match
            if str(match_info.id) != str(LAST_MATCH):
                summoners[i].last_match = match_info.id
            else:
                continue
            
            logging.info(f'Found new game for {summoner.name}')

            # Second API Call to check game stats
            response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matches/' + str(match_info.id) + '?&api_key=' + RIOT_KEY)
            match_summary = json.loads(response.text)

            # Determine which participant is the current summoner and assign info
            summoner_stats_info = None
            parts = match_summary['participants']
            for p in parts:
                if str(p['championId']) == str(most_recent_match['matches'][0]['champion']) and str(p['timeline']['role']) == str(match_info.role) and str(p['timeline']['lane']) == str(match_info.lane):
                    summoner_stats_info = p

            # Grab info we want from stats
            match_info.kills = summoner_stats_info['stats']['kills']
            match_info.deaths = summoner_stats_info['stats']['deaths']
            match_info.assists = summoner_stats_info['stats']['assists']
            match_info.duration = match_summary['gameDuration']
            match_info.date = match_summary['gameCreation']
            
            # Determine if on the leaderboard and store index in update_index
            prev_leaderboard = database.get_top_ints(g[0])
            update_index = -1
            for j, slot in enumerate(prev_leaderboard):
                if slot[6] < match_info.deaths:
                    update_index = j + 1
                elif slot[6] == match_info.deaths and slot[5] > match_info.kills:
                    update_index = j + 1
                elif slot[6] == match_info.deaths and slot[5] == match_info.kills and match_info.assists > match_info.assists:
                    update_index = j + 1
            
            # Adding to database
            database.add_match(g[0], match_info)
            
            # Getting channel to message
            if CHANNEL == '':
                return
            channel = bot.get_channel(int(CHANNEL))

            # Sending a Discord message based on number of deaths
            if is_int(match_info.kills, match_info.deaths, match_info.assists):
                logging.info(f'Sending a Discord message for {summoner.name}...')
                if match_info.deaths >= 20:
                    msg = random.choice(int_messages['turbo-mega'])
                elif match_info.deaths >= 15:
                    msg = random.choice(int_messages['turbo'])
                elif match_info.deaths >= 10:
                    msg = random.choice(int_messages['heavy'])
                else:
                    msg = random.choice(int_messages['standard'])
                    
                # Replacing variables in template
                msg = msg.replace('?s?', summoner.name)
                msg = msg.replace('?S?', summoner.name.upper())
                msg = msg.replace('?d?', str(match_info.deaths))
                msg = msg.replace('?k?', str(match_info.kills))
                msg = msg.replace('?a?', str(match_info.assists))
                
                await channel.send(msg)
                
                # Sending leaderboard message if necessary
                if update_index != -1:
                    await channel.send(f'This is now **#{update_index}** on the int leaderboard!')

            
            # Update Summoner table
            database.update_summoner_match(g[0], summoner.id, match_info.id)
        

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
    logging.info(f'{bot.user.name} has connected to Discord!')
    get_int.start()


if __name__ == '__main__':
    
    # Logging configuration
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO, filename='test.log')
        
    # Checking if database exists
    if not os.path.isfile('jit.db'):
        database.create_database()
        database.create_match_table()
        database.create_summoner_table()
        
    # Checking if environment file exists
    if not os.path.isfile('.env'):
        # Int Updates
        print('Thank you for using Jon Int Tracker (JIT).\nPlease provide the following details to setup the bot.  You can always change the .env file manually afterwards.')
        DISCORD_TOKEN = input('Enter your Discord bot token: ')
        RIOT_KEY = input('Enter your Riot API key: ')
        CHANNEL = ''

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

    # Loading bot extensions
    bot.load_extension("summoners")
    bot.load_extension("leaderboard")

    bot.run(TOKEN)
