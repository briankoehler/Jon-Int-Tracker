# leaderboard.py
import pickle
import requests, json
from datetime import date
from discord.ext import commands

class Match:
    def __init__(self, champ_id, summoner, kills, deaths, assists):
        response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json')
        champions = json.loads(response.text)
        self.champ_id = champ_id
        for champion in champions['data']:
            if champions['data'][champion]['key'] == str(champ_id):
                self.champ = champion
        self.summoner = summoner
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.date = date.today()

def load_leaderboard():
    """Reads leaderboard pickle

    Returns:
        List: Contains the top 10 int matches
    """
    leaderboard_file = open('leaderboard.pkl', 'rb')
    data = pickle.load(leaderboard_file)

    leaderboard_matches = []
    for match in data:
        new_match = Match(match.champ_id, match.summoner, match.kills, match.deaths, match.assists)
        leaderboard_matches.append(new_match)
    return leaderboard_matches

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
    while i < len(leaderboard_matches):
        if m.deaths > leaderboard_matches[i].deaths:
            leaderboard_matches.insert(i, m)
            updated = True
            break
        if m.deaths == leaderboard_matches[i].deaths:
            if m.kills < leaderboard_matches[i].kills:
                leaderboard_matches.insert(i, m)
                updated = True
                break
        i += 1
    if updated:
        del leaderboard_matches[len(leaderboard_matches) - 1]
    write_leaderboard(leaderboard_matches)

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
            leaderboard_string += f'**{num})** {match.kills}/{match.deaths}/{match.assists} - {match.summoner} ({match.champ})\n'
            num = num + 1
        await ctx.send(leaderboard_string)

def setup(bot):
    bot.add_cog(LeaderBoardCog(bot))