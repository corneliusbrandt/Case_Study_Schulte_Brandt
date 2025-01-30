import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__)))
sys.path.append(str(pathlib.Path(__file__).parent))

import os
from tinydb import TinyDB, Query
from serializer_file import serializer

def find_devices() -> list:
    """Find all devices in the database."""
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('devices')
    result = db_connector.all()
    
    if result:
        result = [x["device_name"] for x in result]
    
    return result

def find_users() -> list:
    """Find all users in the database."""
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('users')
    result = db_connector.all()
    
    return result

def find_maintenance() -> list:
    """Find all maintenance entries in the database."""
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('maintenance')
    result = db_connector.all()
    
    return result

if __name__ == "__main__":
    print(find_devices())