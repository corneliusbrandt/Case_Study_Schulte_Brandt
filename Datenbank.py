from tinydb import TinyDB, Query
import os

DB_FILE = 'device_manager.json'
db = TinyDB(os.path.join(os.path.dirname(__file__), DB_FILE))


class User:
    def __init__(self):
        self.table = db.table('users')

    def add(self, name, email):
        if not self.table.search(Query().email == email):
            self.table.insert({'name': name, 'email': email})

    def get_all(self):
        return self.table.all()

class Device:
    def __init__(self):
        self.table = db.table('devices')

    def add(self, name, responsible, end_of_life, maintenance_interval, maintenance_cost, status):
        self.table.insert({
            'name': name,
            'responsible': responsible,
            'end_of_life': end_of_life.strftime('%Y-%m-%d'),
            'maintenance_interval': maintenance_interval,
            'maintenance_cost': maintenance_cost,
            'status': status
        })

    def get_all(self):
        return self.table.all()

class Reservation:
    def __init__(self):
        self.table = db.table('reservations')

    def add(self, user_id, device_id, start_time, end_time):
        conflicts = self.table.search((Query().device_id == device_id) &
                                       (Query().start_time < end_time.isoformat()) &
                                       (Query().end_time > start_time.isoformat()))
        if conflicts:
            return False

        self.table.insert({
            'user_id': user_id,
            'device_id': device_id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        })
        return True

    def get_all(self):
        return self.table.all()