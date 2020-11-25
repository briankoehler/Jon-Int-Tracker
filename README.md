# Jon-Int-Tracker
Discord bot to provide updates when specified summoners have a bad game on Summoner's Rift in League of Legends.  Also creates a leaderboard of the worst games.  Inspiried by my friend Jon, who ints League of Legends games a lot.
## Setup
I'm still learning how to package Python projects (and Python in general).  Use the following command to get the dependencies.
```
pipenv install
```
# Execution
Once you want to run the bot:
```
pipenv shell
cd bot
python3 bot.py
```
Upon first time running, you will be prompted for your Discord token, Channel ID, Riot Games API key, and a kill-death difference (to determine whether or not an int - will be replaced in the future).
Unless you have a permanent Riot Games API key, you will have to update your Riot Games API key every 24 hours with within the ```.env``` file.
# Error Getting Match Info
If tracking more than 8 summoners, you will likely need to adjust the time interval of the ```get_int()``` task located inside ```bot/bot.py```.  This is a simple task, and can be done by opening ```bot.py``` and finding the following on line 46:
```
@tasks.loop(seconds=10)
```
Simply change the 10 to a higher number (such as 20) and you will have no issues.
# Planned Features
* Total stats per summoner
* More leaderboards
* More "poor game" message formats
