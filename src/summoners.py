# summoners.py
import pickle
import datetime
from datetime import date

class Summoner:
    def __init__(self, id, name, encrypted_id, last_game_id):
        self.id = id
        self.name = name
        self.encrypted_id = encrypted_id
        self.last_game_id = last_game_id

def logg(message):
    """Prints a message to the console with date/time

    Args:
        message (String): Message to print
    """
    print(f'[{datetime.datetime.now()}] {message}')

def load_summoners():
    """Loads the summoners pickle

    Returns:
        Tuple: # of summoners, summoners list
    """
    try:
        pickle_file = open('summoners.pkl', 'rb')
    except:
        logg('Summoners file not found...') # Change this
        return
    return pickle.load(pickle_file), pickle.load(pickle_file)

def update_summoners(summoners_list):
    """Updates the summoners pickle

    Args:
        summoners_list (List): List containing summoners to track
    """
    with open('summoners.pkl', 'wb') as output:
        pickle.dump(len(summoners_list), output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(summoners_list, output, pickle.HIGHEST_PROTOCOL)