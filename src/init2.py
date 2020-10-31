# init.py
import requests, json
import pickle


class Summoner:
    def __init__(self, name, encryptedId, last_game_id):
        self.name = name
        self.encryptedId = encryptedId
        self.last_game_id = last_game_id

summoners_names_list = []
summoners_list = []


def main():
    # Int Updates
    print('Thank you for using Jon Int Tracker (JIT).\nAnswers to the following questions will be to track inting of a user.')
    DISCORD_TOKEN = input('Enter your Discord API token: ')
    DISCORD_CHANNEL = input('Enter your Discord Channel ID: ')
    RIOT_KEY = input('Enter your Riot API key: ')
    DIFF = input('Enter necessary kill-death difference: ')

    # Getting Summoner Names
    while True:
        num = int(input('Enter how many people to track: '))
        if num < 0:
            print('Please enter a nonnegative integer')
            continue
        NUM_OF_INTERS = num
        break
    for i in range(NUM_OF_INTERS):
        summoner = input(f'Enter summoner #{i + 1} name: ')
        summoners_names_list.append(summoner)

    # Retrieving Encyrpted IDs
    for s in summoners_names_list:
        response = requests.get(url='https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + s + '?api_key=' + RIOT_KEY)
        account_info = json.loads(response.text)
        sumId = account_info['accountId']
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + sumId + '?endIndex=1&beginIndex=0&api_key=' + RIOT_KEY)
        most_recent_match = json.loads(response.text)
        game_id = most_recent_match['matches'][0]['gameId']
        newSum = Summoner(s, sumId, game_id)
        summoners_list.append(newSum)

    # Dumping list of summoner objects to pickle file
    with open('../leaderboard_summoners.pkl', 'wb') as output:
        pickle.dump(len(summoners_list), output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(summoners_list, output, pickle.HIGHEST_PROTOCOL)

    # Writing .env file
    with open('.env', 'w') as file:
        file.write('# .env\n\n')
        file.write('# Discord Variables\n')
        file.write(f'DISCORD_TOKEN="{DISCORD_TOKEN}"\n')
        file.write(f'DISCORD_CHANNEL="{DISCORD_CHANNEL}"\n')
        file.write('\n')
        file.write('# Riot Variables\n')
        file.write(f'RIOT_KEY="{RIOT_KEY}"\n')
        file.write('\n')
        file.write('# App Variables\n')
        file.write(f'DIFF="{DIFF}"\n')

if __name__ == "__main__":
    main()