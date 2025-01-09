import os
from tinydb import TinyDB, Query
from serializer_file import serializer

def find_devices() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('devices')
    # Search the database for all devices that are active
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["device_name"] for x in result]
    
    return result

def find_users() -> list:
    """Find all users in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('users')
    # Search the database for all users
    result = db_connector.all()
    
    return result

if __name__ == "__main__":
    print(find_devices())