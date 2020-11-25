# init.py
import pickle
from summoners import Summoner
from leaderboard import Match
from bot import Game


def main():

    # Int Updates
    print('Thank you for using Jon Int Tracker (JIT).\nPlease provide the following details to setup the bot.  You can always change the .env file manually afterwards.')
    DISCORD_TOKEN = input('Enter your Discord API token: ')
    DISCORD_CHANNEL = input('Enter your Discord Channel ID: ')
    RIOT_KEY = input('Enter your Riot API key: ')
    DIFF = input('Enter necessary kill-death difference: ')

    # Writing .env file
    with open('.env', 'w') as file:
        file.write('# .env\n\n')
        file.write(f'DISCORD_TOKEN="{DISCORD_TOKEN}"\n')
        file.write(f'DISCORD_CHANNEL="{DISCORD_CHANNEL}"\n')
        file.write(f'RIOT_KEY="{RIOT_KEY}"\n')
        file.write(f'DIFF="{DIFF}"\n')

    # Initializing leaderboard file
    matches = []
    for i in range(10):
        matches.append('')

    # Leaderboard Creation
    with open('leaderboard.pkl', 'wb') as output:
        pickle.dump(matches, output, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    main()