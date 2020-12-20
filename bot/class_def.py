# class_def.py
import requests, json
from bs4 import BeautifulSoup
from datetime import date

class Match:
    def __init__(self, game_id, champ_id, summoner, kills, deaths, assists):
        
        page = requests.get('https://leagueoflegends.fandom.com/wiki/Patch')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        wikitable = soup.find_all('table', class_='wikitable')
        wikitable = wikitable[0]
        patch = wikitable.find_all('a')
        patch = patch[0]
        patch = patch.text
        patch = patch + '.1'
        
        response = requests.get(url=f'http://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json')
        champions = json.loads(response.text)
        
        self.champ_id = champ_id
        for champion in champions['data']:
            if champions['data'][champion]['key'] == str(champ_id):
                self.champ = champion
                
        self.game_id = game_id
        self.summoner = summoner
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.date = date.today()
        
class Summoner:
    def __init__(self, name, encrypted_id, last_game_id):
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
