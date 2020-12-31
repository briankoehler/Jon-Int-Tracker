# summoners.py
import os
import requests, json
from discord.ext import commands
from database import get_summoners, add_summoner, remove_summoner
from class_def import Summoner


class SummonersCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # List Summoners being tracked
    @commands.command()
    async def list(self, ctx):
        """Sends a message with all summoners being tracked"""

        # Retrieving summoners from database
        summoners = get_summoners(ctx.guild.id)

        # Checking if any summoners being tracked
        if len(summoners) == 0:
            await ctx.send('No summoners being tracked.  Use ?add to add some.')
            return

        # Initialization
        summoners_string = '_ _\n\n**SUMMONERS BEING TRACKED**\n--------------------\n'

		# Appending the message string
        for s in summoners:
            summoners_string += f'• {s[2]}\n'
            
        await ctx.send(summoners_string)


    # Add a new Summoner to keep track of
    @commands.command()
    async def add(self, ctx, *args):
        """Adds a summoner to the tracking list

        Args:
            name (String): Name of summoner to add
        """

        name = " ".join(args[:])

        # Get account information
        RIOT_KEY = os.getenv('RIOT_KEY')
        response = requests.get(url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + name + '?api_key=' + RIOT_KEY)
        account_info = json.loads(response.text)
        try:
            sum_id = account_info['accountId']
        except:
            await ctx.send(f'Could not find **{name}**')
            return
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + sum_id + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
        most_recent_match = json.loads(response.text)
        game_id = most_recent_match['matches'][0]['gameId']

        # Check if account already in database
        database_summoners = get_summoners(ctx.guild.id)
        for s in database_summoners:
            if s[1] == sum_id:
                await ctx.send(f'**{name}** is already being tracked.')
                return
            
        # Adding to database
        new_sum = Summoner(sum_id, name, game_id)
        add_summoner(ctx.guild.id, new_sum)

        await ctx.send(f'Added **{name}** to tracking list.')


    # Remove a summoner being tracked
    @commands.command()
    async def remove(self, ctx, *args):
        """Removes a summoner from traking list

        Args:
            args (String): Name of summoner to remove
        """

        name = " ".join(args[:])

        # Removing from database
        did_remove = remove_summoner(ctx.guild.id, name)

        if did_remove:
            await ctx.send(f'Removed **{name}** from tracking list.')
            return
        await ctx.send(f'Unable to find **{name}** in tracking list.')


def setup(bot):
    bot.add_cog(SummonersCog(bot))
