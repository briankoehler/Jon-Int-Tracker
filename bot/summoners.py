# summoners.py
import pickle
import datetime, os
import requests, json
from discord.ext import commands
from datetime import date
from class_def import Summoner, Game


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

        # Retrieving summoner info from pickle
        number_of_sums, summoners_list = load_summoners()

        # Checking if any summoners being tracked
        if number_of_sums == 0:
            await ctx.send('No summoners being tracked.  Use ?add to add some.')
            return

        # Initialization
        summoners_string = '_ _\n\n**SUMMONERS BEING TRACKED**\n--------------------\n'

        # Adding Summoner names to string of message to send
        for i in range(number_of_sums):
            summoners_string += f'• {summoners_list[i].name}\n'
        await ctx.send(summoners_string)


    # Add a new Summoner to keep track of
    @commands.command()
    async def add(self, ctx, *args):
        """Adds a summoner to the tracking list

        Args:
            name (String): Name of summoner to add
        """

        name = " ".join(args[:])

        # Retrieving summoner info from pickle
        number_of_sums, summoners_list = load_summoners()

        for s in summoners_list:
            if s.name == name:
                await ctx.send(f'**{name}** is already being tracked.')
                return

        RIOT_KEY = os.getenv('RIOT_KEY')
        response = requests.get(url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + RIOT_KEY)
        account_info = json.loads(response.text)
        try:
            sumId = account_info['accountId']
        except:
            await ctx.send(f'Could not find **{name}**')
            return
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + sumId + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
        most_recent_match = json.loads(response.text)
        game_id = most_recent_match['matches'][0]['gameId']

        newSum = Summoner(name, sumId, game_id)
        summoners_list.append(newSum)
        # Dumping list of summoner objects to pickle file
        update_summoners(summoners_list)

        await ctx.send(f'Added **{name}** to tracking list.')

    # Remove a summoner being tracked
    @commands.command()
    async def remove(self, ctx, args):
        """Removes a summoner from traking list

        Args:
            args (String): Name of summoner to remove
        """

        name = " ".join(args[:])

        # Retrieving summoner info from pickle
        number_of_sums, summoners_list = load_summoners()
        
        found = False
        for i, summoner in enumerate(summoners_list):
            if summoner.name == name:
                found = True
                del summoners_list[i]

        # Dumping list of summoner objects to pickle file
        update_summoners(summoners_list)

        if found:
            await ctx.send(f'Removed {name} from tracking list.')
            return
        await ctx.send(f'Unable to find {name} in tracking list.')


def setup(bot):
    bot.add_cog(SummonersCog(bot))
