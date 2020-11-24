# Jon-Int-Tracker
Discord bot to provide updates when specified summoners have a bad game on Summoner's Rift in League of Legends.  Also creates a leaderboard of the worst games.  Inspiried by my friend Jon, who ints League of Legends games a lot.
## Setup
I'm still learning how to package Python projects (and Python in general), but in the meantime I have created an init.py file.  I've also included a Pipfile to install dependencies.  Use the following command to get the dependencies.
```
pipenv install
```

Run the following before attempting to use the bot:
```
cd src
python3 init.py
```
It will prompt you for your Discord API token, your Riot Games API key, your Discord Channel ID, and your desired kill-death difference.  Kill-death difference determines whether or not an update is provided for a game.

Once you want to run the bot:
```
cd src
python3 bot.py
```
Unless you have a permanent Riot Games API key, you will have to update your Riot Games API key every 24 hours with ```init.py```.
