# class_def.py

class Match:
        
    def __init__(self, id, summoner, champ, role, lane, queue):
        
        self.id = id
        self.summoner = summoner
        self.champ = champ
        self.role = role
        self.lane = lane
        self.queue = queue
        

class Summoner:

    def __init__(self, id, name, last_match):
        
        self.id = id
        self.name = name
        self.last_match = last_match
