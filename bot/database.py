# database.py
import sqlite3

# DATABASE CREATION
def create_database():
    """Creates the SQLite database"""
    conn = sqlite3.connect('jit.db')
    

# MATCH TABLE
def create_match_table():
    """Creates table to hold all matches"""
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE match(
            guild TEXT NOT NULL,
            id TEXT NOT NULL,
            duration INTEGER CHECK(duration > -1),
            date INTEGER CHECK(date > -1),
            summoner TEXT NOT NULL,
            champ TEXT NOT NULL,
            kills INTEGER CHECK(kills > -1),
            deaths INTEGER CHECK(deaths > -1),
            assists INTEGER CHECK(deaths > -1),
            role TEXT NOT NULL,
            lane TEXT NOT NULL,
            queue INTEGER CHECK(queue > -1));
    ''')
    
    
def add_match(guild, match):
    """Inserts match data into database

    Args:
        guild (int): ID of guild
        match (Match): Match to add to database
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, match.id, match.duration, match.date, 
            match.summoner, match.champ, match.kills, match.deaths, 
            match.assists, match.role, match.lane, match.queue)
    
    c.execute(''' 
        INSERT INTO match
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', data)
    
    conn.commit()
    
    
def get_top_ints(guild):
    """Find the top 10 "ints"

    Args:
        guild (int): ID of guild

    Returns:
        tuple: Top 10 "ints"
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
        WITH t1 AS (SELECT * FROM match WHERE guild == ? ORDER BY deaths DESC, kills ASC, assists ASC)
            
        SELECT * FROM t1 LIMIT 10;
        ''', (guild,))
    
    top_ints = c.fetchall()
    return top_ints


# SUMMONER TABLE
def create_summoner_table():
    """Creates a table to hold all summoners' information"""
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE summoner(
            guild TEXT NOT NULL,
            id TEXT NOT NULL,
            name TEXT NOT NULL,
            last_match TEXT NOT NULL,
            PRIMARY KEY (guild, id));
        ''')
    

def get_summoners(guild):
    """Get all summoners being tracked by a guild

    Args:
        guild (int): ID of guild

    Returns:
        tuple: All summoners being tracked by specified guild
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
            SELECT * FROM summoner WHERE guild = ?
            ''', (guild,))
    
    summoners = c.fetchall()
    return summoners
    
    
def add_summoner(guild, summoner):
    """Adds a summoner to the database

    Args:
        guild (int): ID of guild
        summoner (Summoner): Summoner to add to database
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, summoner.id, summoner.name, summoner.last_match)
    
    c.execute('''
        INSERT INTO summoner
        VALUES (?, ?, ?, ?);
        ''', data)
    conn.commit()
    

def remove_summoner(guild, name):
    """Removes a summoner from the database

    Args:
        guild (int): ID of guild
        name (str): Name of player to remove

    Returns:
        bool: Whether or not there was a deletion
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (guild, name)
    
    c.execute('''
        DELETE FROM summoner WHERE guild = ? and name = ?
        ''', data)
    
    if c.rowcount == 1:
        conn.commit()
        return True
    else:
        return False


def update_summoner_match(guild, summoner, match):
    """Updates the last match ID of a summoner

    Args:
        guild (int): ID of guild
        summoner (str): ID of summoner
        match (int): ID of latest match
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (match, guild, summoner)
    
    c.execute('UPDATE summoner SET last_match = ? WHERE guild = ? AND id = ?', data)
    conn.commit()
    
    
def get_summoner_name_from_id(summoner):
    """Obtain a summoner name from the table given the summoner's ID

    Args:
        summoner (int): ID of summoner

    Returns:
        str: Name of desired summoner
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('SELECT name FROM summoner WHERE id = ?', (summoner,))
    name = c.fetchall()[0][0]
    return name
    

# GUILD TABLE
def create_guild_table():
    """Creates table to hold all guilds"""
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE guild(
            id TEXT PRIMARY KEY,
            channel TEXT);
        ''')


def add_guild(guild):
    """Adds a guild to the guild table

    Args:
        guild (int): ID of guild
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO guild (id)
        VALUES (?);
        ''', (guild,))
    conn.commit()
    

def remove_guild(guild):
    """Removes a guild from the guild table

    Args:
        guild (int): ID of guild
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM guild WHERE id = ?', (guild,))
    conn.commit()
    

def update_guild_channel(guild, channel):
    """Changes the specified guild's notification channel

    Args:
        guild (int): ID of guild
        channel (int): ID of new channel
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    data = (channel, guild)
    
    c.execute('''
        UPDATE guild 
        SET channel = ? 
        WHERE id = ?
        ''', data)
    conn.commit()
    
    
def get_guilds():
    """Obtain a tuple of all guild 

    Returns:
        tuple: All guilds with summoners in database
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('SELECT DISTINCT id FROM guild')
    guilds = c.fetchall()
    return guilds
    

def get_channel(guild):
    """Gets the notification channel specified by a guild

    Args:
        guild (int): ID of guild

    Returns:
        [int]: ID of text channel for notifications
    """
    
    conn = sqlite3.connect('jit.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM guild WHERE id = ?', (guild,))
    info = c.fetchall()
    return info[0][1]
