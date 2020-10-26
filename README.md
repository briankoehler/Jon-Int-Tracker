# Jon-Int-Tracker
Discord bot to provide updates on my friend Jon's League of Legends games.  Jon is a strong inter, so I thought it'd be funny to receive updates on his games when each match finishes.
## Setup
I'm still learning how to package Python projects (and Python in general), but in the meantime I have created an init.py file.  I've also included a Pipfile to install dependencies.  Use the following command to get the dependencies.
```
pipenv install
```

Run the following before attempting to use the bot:
```
python3 init.py
```
It will prompt you for your Discord API token, your Discord guild name (not important at the moment), your Riot Games API key, and your desired kill-death difference.  Kill-death difference determines whether or not an update is provided for a game.
