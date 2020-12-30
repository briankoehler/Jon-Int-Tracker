# leaderboard.py
from class_def import Match
from database import get_top_ints
from discord.ext import commands


class LeaderBoardCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot


    # Leaderboard Command
    @commands.command()
    async def leaderboard(self, ctx):
        """Sends a message with the top 10 int matches"""

        # Query database and get a tuple
        top_ints = get_top_ints(ctx.guild.id)

        # Formulating leaderboard message
        leaderboard_string = '_ _\n\n**INT LEADERBOARD**\n--------------------\n'
        i = 0
        for i, match in enumerate(top_ints):
            leaderboard_string += f'**{i + 1})** {match[5]}/{match[6]}/{match[7]} - {match[3]} ({match[4]})\n_ _' # k/d/a - summoner (champion)

        # Adding any blank lines
        if i + 1 != 10:
            while i != 10:
                leaderboard_string += f'**{i + 1})**\n'
                i += 1

        await ctx.send(leaderboard_string)


def setup(bot):
    bot.add_cog(LeaderBoardCog(bot))
