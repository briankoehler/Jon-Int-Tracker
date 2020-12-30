# database.py
import sqlite3


def create_database():
    """Creates the SQLite database"""
    conn = sqlite3.connect('jit.db')
    
    
def create_match_table():
    """Creates table to hold all matches

    Returns:
        bool: Whether or not query succeeded
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                CREATE TABLE match(
                    guild TEXT NOT NULL,
                    id TEXT NOT NULL,
                    duration INTEGER CHECK(duration > -1)
                    date INTEGER CHECK(date > 0)
                    summoner TEXT NOT NULL,
                    champ TEXT NOT NULL,
                    kills INTEGER CHECK(kills > -1),
                    deaths INTEGER CHECK(deaths > -1),
                    assists INTEGER CHECK(deaths > -1),
                );
                ''')
        return True
    
    except:
        return False
    
    
def add_match(guild, match):
    """Inserts match data into database

    Args:
        guild (str): ID of guild
        match (Match): Match to add to database

    Returns:
        bool: Whether or not transaction was successful
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, match.id, match.duration, match.summoner, match.champ, match.kills, match.deaths, match.assists, match.date,)
    
    try:
        c.execute(f''' 
                  INSERT INTO match
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                  ''', data)
        
        conn.commit()
        return True
    
    except:
        return False
    
    
def get_top_ints(guild):
    """Find the top 10 "ints"

    Args:
        guild (str): ID of guild

    Returns:
        tuple: Top 10 "ints"
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                WITH t1 AS (SELECT * FROM match WHERE guild == ? ORDER BY deaths DESC)
                
                SELECT * FROM t1 LIMIT 10;
                ''', (guild,))
        
        top_ints = c.fetchall()
        return top_ints
    
    except:
        return []


def create_summoner_table():
    """Creates a table to hold all summoners' information

    Returns:
        bool: Whether or not query succeeded
    """
    
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
    

def get_summoners(guild):
    """Get all summoners being tracked by a guild

    Args:
        guild (str): ID of guild

    Returns:
        tuple: All summoners being tracked by specified guild
    """
    
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
    
    
def add_summoner(guild, summoner):
    """Adds a summoner to the database

    Args:
        guild (str): ID of guild
        summoner (Summoner): Summoner to add to database

    Returns:
        bool: Whether or not transaction succeeded
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, summoner.id, summoner.name, summoner.last_match)
    
    try:
        c.execute('''
                INSERT INTO summoner
                VALUES (?, ?, ?, ?);
                ''', data)
        conn.commit()
        return True
        
    except:
        return False
    

def remove_summoner(guild, name):
    """Removes a summoner from the database

    Args:
        guild (str): ID of guild
        name (str): Name of player to remove

    Returns:
        bool: Whether or not transaction succeeded and their was a deletion
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, name)
    
    try:
        c.execute('''
                  DELETE FROM summoner WHERE guild = ? and name = ?
                  ''', data)
        
        if c.rowcount == 1:
            conn.commit()
            return True
        else:
            return False
        
    except:
        return False


def update_summoner_match(guild, id, match):
    """Updates the last match ID of a summoner

    Args:
        guild (str): ID of guild
        id (str): ID of summoner
        match (int): ID of latest match

    Returns:
        bool: Whether or not transaction succeeded
    """
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (match, guild, id)
    
    try:
        c.execute('''
                  UPDATE summoner SET last_match = ? WHERE guild = ? AND id = ?
                  ''', data)
        conn.commit()
        return True
    
    except:
        return False
    
    
def get_guilds():
    """Obtain a tuple of all guild 

    Returns:
        tuple: All guilds with summoners in database
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    try:
        c.execute('''
                  SELECT DISTINCT guild FROM summoner
                  ''')
        guilds = c.fetchall()
        return guilds
    
    except:
        return False