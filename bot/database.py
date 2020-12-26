import datetime
import sqlite3
from class_def import Match
from datetime import date


def create_database():
    conn = sqlite3.connect('jit.db')
    
    
def create_match_table():
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                CREATE TABLE match(
                    guild TEXT NOT NULL,
                    id TEXT NOT NULL,
                    duration INTEGER CHECK(duration > -1),
                    summoner TEXT NOT NULL,
                    champ TEXT NOT NULL,
                    kills INTEGER CHECK(kills > -1),
                    deaths INTEGER CHECK(deaths > -1),
                    assists INTEGER CHECK(deaths > -1)
                );
                ''')
        return True
    
    except:
        return False
    
    
def add_match(guild, match):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, match.id, match.duration, match.summoner, match.champ, match.kills, match.deaths, match.assists)
    
    try:
        c.execute(f''' 
                  INSERT INTO int
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                  ''', data)
        
        conn.commit()
        return True
    
    except:
        return False
    
    
def get_top_ints(guild):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                WITH t1 AS (SELECT * FROM int WHERE guild == ? ORDER BY deaths DESC)
                
                SELECT * FROM t1 LIMIT 10;
                ''', (guild,))
        
        top_ints = c.fetchall()
        return top_ints
    
    except:
        return []


def create_summoners_table():
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                CREATE TABLE summoner(
                    guild TEXT NOT NULL,
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    last_match TEXT NOT NULL
                );
                ''')
        return True
        
    except:
        return False
    
    
def add_summoner(guild, summoner):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, summoner.id, summoner.name, summoner.last_match)
    
    try:
        c.execute('''
                INSERT INTO summoner
                VALUES (?, ?, ?, ?);
                ''', data)
        return True
        
    except:
        return False
    
    
def get_summoners(guild):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                SELECT * FROM summoner WHERE guild = ?
                ''', (guild,))
        
        summoners = c.fetchall()
        return summoners
    
    except:
        return []

def remove_summoner(guild, name):
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, name)
    
    try:
        c.execute('''
                  DELETE FROM summoner WHERE guild = ? and name = ?
                  ''', data)
        return True
        
    finally:
        return False
