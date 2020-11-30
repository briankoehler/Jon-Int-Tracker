# leaderboard.py
import pickle
import requests, json
from datetime import date
from discord.ext import commands
from class_def import Match


def load_leaderboard():
    """Reads leaderboard pickle

    Returns:
        List: Contains the top 10 int matches
    """
    leaderboard_file = open('leaderboard.pkl', 'rb')
    data = pickle.load(leaderboard_file)
    return data


def write_leaderboard(matches):
    """Writes matches to the leaderboard pickle

    Args:
        matches (List): Contains new top 10 int matches
    """
    with open('leaderboard.pkl', 'wb') as output:
        pickle.dump(matches, output, pickle.HIGHEST_PROTOCOL)


def update_leaderboard(m):
    """Determines whether or not m should be added to leaderboard pickle and does so if necessary

    Args:
        m (Match): Pending match that may be added to learboard pickle
    """
    leaderboard_matches = load_leaderboard()
    updated = False
    i = 0
    update_index = -1
    while i < len(leaderboard_matches): # TODO: Account for exact same stats (or just leave as is)
        if isinstance(leaderboard_matches[i], str):
            leaderboard_matches[i] = m
            update_index = i
            break
        if m.deaths > leaderboard_matches[i].deaths:
            leaderboard_matches.insert(i, m)
            updated = True
            update_index = i
            break
        if m.deaths == leaderboard_matches[i].deaths:
            if m.kills < leaderboard_matches[i].kills:
                leaderboard_matches.insert(i, m)
                updated = True
                update_index = i
                break
            if m.kills == leaderboard_matches[i].kills:
                if m.assists < leaderboard_matches[i].assists:
                    leaderboard_matches.insert(i, m)
                    updated = True
                    update_index = i
                    break
        i += 1
    if updated:
        del leaderboard_matches[len(leaderboard_matches) - 1]
    write_leaderboard(leaderboard_matches)
    return update_index


class LeaderBoardCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # Leaderboard Command
    @commands.command()
    async def leaderboard(self, ctx):
        """Sends a message with the top 10 int matches"""

        leaderboard_list = load_leaderboard()
        leaderboard_string = '_ _\n\n**INT LEADERBOARD**\n--------------------\n'
        num = 1
        for match in leaderboard_list:
            if isinstance(match, str):
                leaderboard_string += f'**{num})**\n'
            else:
                leaderboard_string += f'**{num})** {match.kills}/{match.deaths}/{match.assists} - {match.summoner} ({match.champ})\n'
            num = num + 1
        await ctx.send(leaderboard_string)


def setup(bot):
    bot.add_cog(LeaderBoardCog(bot))