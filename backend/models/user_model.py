from datetime import datetime
import json

class User:
    def __init__(self, user_id, username, reading_history=None, preferences=None):
        self.user_id = user_id
        self.username = username
        self.reading_history = reading_history if reading_history is not None else []
        self.preferences = preferences if preferences is not None else {}

    def add_to_reading_history(self, book_id):
        if book_id not in self.reading_history:
            self.reading_history.append(book_id)

    def set_preferences(self, preferences):
        self.preferences = preferences

    def get_reading_history(self):
        return self.reading_history

    def get_preferences(self):
        return self.preferences

def load_users(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_users(file_path, users):
    with open(file_path, 'w') as f:
        json.dump(users, f)