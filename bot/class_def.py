# class_def.py
import requests, json
from datetime import date

class Match:
    def __init__(self, champ_id, summoner, kills, deaths, assists):
        response = requests.get(url='http://ddragon.leagueoflegends.com/cdn/10.24.1/data/en_US/champion.json')
        champions = json.loads(response.text)
        self.champ_id = champ_id
        for champion in champions['data']:
            if champions['data'][champion]['key'] == str(champ_id):
                self.champ = champion
        self.summoner = summoner
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.date = date.today()
        
class Summoner:
    def __init__(self, id, name, encrypted_id, last_game_id):
        self.id = id
        self.name = name
        self.encrypted_id = encrypted_id
        self.last_game_id = last_game_id

class Game:
    def __init__(self, game_id, champion, role, lane, queue):
        self.game_id = game_id
        self.champion = champion
        self.role = role
        self.lane = lane
        self.queue = queue
