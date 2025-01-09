import os

from tinydb import TinyDB, Query
from serializer_file import serializer

class User:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id

    def store_data(self)-> None:
        """Save the user to the database"""
        print("Storing data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.name == self.name)
        if result:
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    def delete(self) -> None:
        """Delete the user from the database"""
        print("Deleting data...")
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.name == self.name)
        if result:
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")
    
    def __str__(self):
        return f"User {self.id} - {self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def find_all(cls) -> list:
        """Find all users in the database"""
        users = []
        for user in User.db_connector.all():
            users.append(User(user['id'], user['name']))
        return users

    @classmethod
    def find_by_attribute(cls, by_attribute : str, attribute_value : str) -> 'User':
        """From the matches in the database, select the user with the given attribute value"""
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery[by_attribute] == attribute_value)
        if result:
            return User(result[0]['id'], result[0]['name'])
        else:
            return None
