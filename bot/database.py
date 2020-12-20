import datetime
import sqlite3
from class_def import Match
from datetime import date


def create_database():
    conn = sqlite3.connect('jit.db')
    
    
def create_int_table():
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
              CREATE TABLE ints(
                  guild_id INTEGER NOT NULL,
                  match_id INTEGER NOT NULL,
                  champ TEXT NOT NULL,
                  summoner_name TEXT NOT NULL,
                  kills INTEGER CHECK(kills > -1),
                  deaths INTEGER CHECK(deaths > -1),
                  assists INTEGER CHECK(deaths > -1)
              );
              ''')
    
    
def add_int(guild_id, new_match):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild_id, new_match.game_id, new_match.champ, new_match.summoner, new_match.kills, new_match.deaths, new_match.assists)
    
    try:
        c.execute(f''' 
                  INSERT INTO ints
                  VALUES (?, ?, ?, ?, ?, ?, ?);
                  ''', data)
        
        conn.commit()
        return True
    except:
        return False
    
    
def get_top_ints(guild_id):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
              WITH guild_ints AS (SELECT * FROM ints WHERE guild_id == ? ORDER BY deaths DESC)
              
              SELECT * FROM guild_ints LIMIT 10;
              ''', (guild_id,))
    
    top_ints = c.fetchall()
    return top_ints


def create_summoners_table():
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
              CREATE TABLE summoners(
                  encrypted_id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  last_game_id TEXT NOT NULL
              );
              ''')
    
def add_summoner():
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
              INSERT INTO summoners
              VALUES (?, ?, ?);
              ''')
