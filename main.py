import sqlite3
import numpy as np
import string
import random
import time
from pynput.keyboard import Key, Listener


class UserTemplate:
    def __init__(self, db_name):
        self.user_id = None
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        # Connect to the SQLite database
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return sqlite3.connect(self.db_name)
    

    def create_table(self):
        # Create a table to store user features if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_features
                               (user_id TEXT, user_name TEXT, event_type TEXT, event_time REAL)''')
        self.connection.commit()

    def generate_paragraph(self):
        # Generate a random paragraph for the user to type
        paragraph = 'The quick brown fox jumped over the lazy dogs and there was nothing to do about it so the owner of the dogs ended up selling the lazy dogs and bougth a a new breed that is a goldberg which is believed to be a special breed'
        return paragraph

    def generate_user_id(self):
        # Generate a unique user ID from user_features (example: first 5 characters)
        return ''.join(random.choices(string.ascii_lowercase, k=5))

    def register_user(self, user_id, user_name):
        # Insert a new user into the database
        self.cursor.execute('''INSERT INTO user_features (user_id, user_name) 
                           VALUES (?, ?)''', (user_id, user_name))
        self.connection.commit()

    # keystrokes stuff
    def store_keystroke_data(self, event_type, event_time):
        # Store keystroke data into the database
        self.connection = self.connect_to_database()  # Create a new connection
        self.cursor = self.connection.cursor()
        self.cursor.execute('''INSERT INTO user_features (user_id, event_type, event_time) 
                           VALUES (?, ?, ?)''', (self.user_id, event_type, event_time))
        self.connection.commit()
      

    def on_press(self, key, event_time):
        # Handler for key press events
        if key == Key.esc:  # Check if the Escape key is pressed
            return False  # Stop listener
        try:
            # Record the key press event time
            self.store_keystroke_data('press', event_time)
        except AttributeError:
            # Ignore special keys
            pass
        return None

    def on_release(self, key, event_time):
        # Handler for key release events
        if key == Key.esc:  # Check if the Escape key is released
            self.connection.close()
            return False  # Stop listener
        # Record the key release event time
        self.store_keystroke_data('release', event_time)
        return None

    def start_capture(self, user_id):
        # Start capturing keystrokes for the specified user
        self.user_id = user_id
        print(self.user_id +"this is the id set to the template")
        with Listener(on_press=lambda k: self.on_press(k, time.time()),
                      on_release=lambda k: self.on_release(k, time.time())) as listener:
            self.connect_to_database()
            listener.join()
            # connection.close()

    def retrieve_user_keystrokes(self, user_id):
        # Retrieve keystroke data for the specified user from the database
        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute('''SELECT event_type, event_time FROM user_features WHERE user_id = ?''', (user_id,))
        keystrokes = cursor.fetchall()
        connection.close()
        return keystrokes

# Example usage:
