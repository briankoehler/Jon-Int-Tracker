# stats.py
from database import get_stats, get_all_games_by_summoner, get_summoners
from class_def import Match
from discord.ext import commands

class StatsCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    # Stats Command
    @commands.command()
    async def stats(self, ctx, *args):
        name = " ".join(args[:])
        
        try:
            stats = get_stats(ctx.guild.id, name)
        except:
            await ctx.send(f'**{name}** is not in the tracking list.  Use ?add to track them.')
            return
        
        if stats[0] == 0:
            await ctx.send(f'**{name}** has not played any games since being added to the list.')
            return
        
        total_playtime = round(stats[1] / 60, 2)
        minutes_per_death = round(total_playtime / stats[3], 2)
        
        get_all_games_by_summoner(ctx.guild.id, name)
        
        msg = f'''_ _\n
            **{name} Statistics**\n
            **Total Games:** {stats[0]}
            **Total Playtime:** {total_playtime} minutes\n
            **Total Kills:** {stats[2]}
            **Total Deaths:** {stats[3]}
            **Total Assists:** {stats[4]}\n
            **Minutes per Death:** {minutes_per_death} min/death'''
            
        await ctx.send(msg)
        
    
def setup(bot):
    bot.add_cog(StatsCog(bot))