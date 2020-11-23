# summoners.py
import pickle
import datetime
import requests, json
from discord.ext import commands
from datetime import date

class Summoner:
    def __init__(self, id, name, encrypted_id, last_game_id):
        self.id = id
        self.name = name
        self.encrypted_id = encrypted_id
        self.last_game_id = last_game_id

    """Prints a message to the console with date/time

    Args:
        message (String): Message to print
    """
    print(f'[{datetime.datetime.now()}] {message}')

def load_summoners():
    """Loads the summoners pickle

    Returns:
        Tuple: # of summoners, summoners list
    """
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        print(f'[{datetime.datetime.now()}] Summoners file not found...')
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

class SummonersCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # List Summoners being tracked
    @commands.command()
    async def list(self, ctx):
        """Sends a message with all summoners being tracked"""

        # Initialization
        summoners_string = '_ _\n\n**SUMMONERS BEING TRACKED**\n--------------------\n'

        # Retrieving summoner info from pickle
        number_of_sums, summoners_list = load_summoners()

        # Adding Summoner names to string of message to send
        for i in range(number_of_sums):
            summoners_string += f'• {summoners_list[i].name} (ID: {summoners_list[i].id})\n'
        await ctx.send(summoners_string)


    # Add a new Summoner to keep track of
    @commands.command()
    async def add(self, ctx, name):
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
        number_of_sums, summoners_list = load_summoners()

        newSum = Summoner(number_of_sums, name, sumId, game_id)
        summoners_list.append(newSum)
        # Dumping list of summoner objects to pickle file
        update_summoners(summoners_list)

        await ctx.send(f'Added **{name}** to tracking list.')


    @commands.command()
    async def remove(self, ctx, name):
        """Removes a summoner from traking list

        Args:
            name (String): Name of summoner to remove
        """

        # Retrieving summoner info from pickle
        number_of_sums, summoners_list = load_summoners()

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

def setup(bot):
    bot.add_cog(SummonersCog(bot))
