# Jon-Int-Tracker
Discord bot to provide updates when specified summoners have a bad game on Summoner's Rift in League of Legends.  Also creates a leaderboard of the worst games.  Inspiried by my friend Jon, who ints League of Legends games a lot.
## Setup
I'm still learning how to package Python projects (and Python in general), but in the meantime I have created an init.py file.  I've also included a Pipfile to install dependencies.  Use the following command to get the dependencies.
```
pipenv install
```
# Execution
Once you want to run the bot:
```
cd bpt
python3 bot.py
```
Upon first time running, you will be prompted for your Discord token, Channel ID, Riot Games API key, and a kill-death difference (to determine whether or not an int - will be replaced in the future).
Unless you have a permanent Riot Games API key, you will have to update your Riot Games API key every 24 hours with within the ```.env``` file.
