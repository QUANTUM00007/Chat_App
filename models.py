from bson.objectid import ObjectId
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # Flask-Login expects .id as string
        self.username = user_data.get('username')

    def get_id(self):
        return self.id 
