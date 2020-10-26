import requests, json
import settings
from twilio.rest import Client
import configparser

###
### NO LONGER BEING USED
###

configggg = configparser.ConfigParser()

# Twilio client setup
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

while True:
    print("ned")
    # API Call
    response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + settings.ACCOUNT_ID + '?endIndex=1&beginIndex=0&api_key=' + settings.RIOT_KEY)
    most_recent_match = json.loads(response.text)

    game_id = most_recent_match['matches'][0]['gameId']
    champion = most_recent_match['matches'][0]['champion']
    role = most_recent_match['matches'][0]['role']
    lane = most_recent_match['matches'][0]['lane']
    queue = most_recent_match['matches'][0]['queue']

    # Check if a solo/duo game (NEEDS TO BE 420)
    if queue == 420:

        # Make sure not an old game
        OLD_ID = configggg['misc']['last_game']
        # TODO: FINISH
        
        # Second API Call to check game stats
        response = requests.get(url='https://na1.api.riotgames.com/lol/match/v4/matches/' + str(game_id) + '?&api_key=' + settings.RIOT_KEY)
        match_summary = json.loads(response.text)

        # Determine which participant is Jon and assign info
        parts = match_summary['participants']
        for p in parts:
            if p['championId'] == champion and p['timeline']['role'] == role and p['timeline']['lane'] == lane:
                jon_info = p

        # Grab info we want from stats
        kills = jon_info['stats']['kills']
        deaths = jon_info['stats']['deaths']

        if deaths - kills >= settings.DIFF:
            message = client.messages.create(
                to = settings.PHONE_NUM,
                from_ = settings.TWILIO_NUM,
                body = 'Jon just WENT OFF with ' + str(kills) + ' KILLS and ' + str(deaths) + ' DEATHS'
            )
            # message = client.messages.create(
            #     to = '+19049558643', # TODO: REMOVE THIS NUMBER
            #     from_ = settings.TWILIO_NUM,
            #     body = 'Jon just WENT OFF with ' + str(kills) + ' KILLS and ' + str(deaths) + ' DEATHS'
            # )