# Jon-Int-Tracker
Discord bot to provide updates when a dynamic list of specified summoners have a bad game on Summoner's Rift in League of Legends.  Also creates a leaderboard of the worst games.  Inspiried by my friend Jon, who ints League of Legends games a lot.

You can invite my bot to your server [here!](https://discord.com/api/oauth2/authorize?client_id=769327183008235540&permissions=8&scope=bot)

![Example](https://imgur.com/a/iGIq0Of)


## Table of Contents
- [Getting Started](https://github.com/briankoehler/Jon-Int-Tracker#getting-started)

- [Customization](https://github.com/briankoehler/Jon-Int-Tracker#customization)

- [Planned Features](https://github.com/briankoehler/Jon-Int-Tracker#planned-features)


## Getting Started
Use the following command to get the bot and its dependencies.
```
git clone https://github.com/briankoehler/Jon-Int-Tracker/
cd Jon-Int-Tracker
pipenv install
```
Retrieve your Riot API key at the [Riot Developer Portal](https://developer.riotgames.com/) and setup an application on the [Discord Developer Portal](https://discord.com/developers/docs/intro) and create a bot for your application there.  Once you want to run the bot:
```
pipenv shell
cd bot
python3 bot.py
```
Upon first time running, you will be prompted for your Discord bot token and Riot Games API key.  Use the ```?help``` command for a list of commands after adding it to your Discord guild.  Unless you have a permanent Riot Games API key, you will have to update your Riot Games API key every 24 hours within the ```.env``` file.


## Customization
### Match Frequency
The frequency of match-checking can be adjusted inside ```bot/bot.py```.  Find the following code snippet inside:
```
@tasks.loop(seconds=20)
async def get_int():
    """Every 20s, check most recent match for every summoner int the summoners pickle and determine if it is an int"""
```
Simply change the number in ```(seconds=20)``` to your desired number of seconds.  **NOTE: Unless you have a public Riot Games API key, you will be severely limited in the number of requests you can submit.  Visit [here](https://developer.riotgames.com/docs/portal#web-apis) to view the restrictions.  Each summoner requires a maximum of 2 requests per check.**

### Message Formats
The notifications sent by the bot can also be customized from within ```bot/int_messages.py```.


## Planned Features
* Better int calculation and leaderboard sorting
* Total stats per summoner
* More leaderboard types
* More "poor game" message formats
