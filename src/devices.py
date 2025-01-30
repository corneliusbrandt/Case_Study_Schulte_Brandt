import os


from tinydb import TinyDB, Query
from serializer_file import serializer
import datetime


class Device():
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('devices')

    # Constructor
    def __init__(self, device_name : str, managed_by_user_id : str, end_of_life=None, maintenance_interval=None, maintanace_last=None, maintenance_cost=None, status=None, maintenance_next=None, doc_id=None) -> None:
        self.device_name = device_name

        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id
        self.end_of_life = end_of_life
        self.maintenance_interval = int(maintenance_interval) if maintenance_interval else 0
        self.maintenance_last = datetime.datetime.now().date() if maintanace_last is None else 0
        self.maintenance_cost = maintenance_cost
        self.status = status
        self.is_active = True
        self.maintenance_next = datetime.datetime.now().date() + datetime.timedelta(days=self.maintenance_interval)
        self.id = doc_id

        
    # String representation of the class
    def __str__(self):
        return f'Device (Object) {self.device_name} ({self.managed_by_user_id})'

    # String representation of the class
    def __repr__(self):
        return self.__str__()
    
    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")
    
    def delete(self):
        print("Deleting data...")
        # Check if the device exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        if result:
            # Delete the record from the database
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            device_results = [cls(d['device_name'], d['managed_by_user_id']) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

    @classmethod
    def find_all(cls) -> list:
        devices = []
        for device_data in Device.db_connector.all():
            devices.append(Device(device_data['device_name'], device_data['managed_by_user_id']))
        return devices
    
    @classmethod
    def find_maintenance(cls) -> list:
        """Find all maintenance entries in the database."""
        maintanance = []
        for maintenance_data in Device.db_connector.all():
            print(maintenance_data['maintenance_cost'])
            maintanance.append(Device(maintenance_data['device_name'], maintenance_data['managed_by_user_id'], maintenance_data['end_of_life'], maintenance_data['maintenance_interval'], maintenance_data['maintenance_last'], maintenance_data['maintenance_cost'], maintenance_data['status'], maintenance_data['maintenance_next'],maintenance_data.doc_id))
        return maintanance
        
    @classmethod
    def update_maintenance(cls):
        """Update maintenance entries in the database."""
        maintance_cost_next_month = 0
        for device_data in Device.db_connector.all():
            maintenance_next_month = datetime.datetime.now().date() + datetime.timedelta(days=30)
            print(type(maintenance_next_month))
            print(type(device_data['maintenance_next']))
            if device_data['maintenance_next'] <= maintenance_next_month:
                maintance_cost_next_month += int(device_data['maintenance_cost'])

        return maintance_cost_next_month

if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1", "one@mci.edu")
    device2 = Device("Device2", "two@mci.edu") 
    device3 = Device("Device3", "two@mci.edu") 
    device4 = Device("Device4", "two@mci.edu") 
    device1.store_data()
    device2.store_data()
    device3.store_data()
    device4.store_data()
    device5 = Device("Device3", "four@mci.edu") 
    device5.store_data()

    #loaded_device = Device.find_by_attribute("device_name", "Device2")
    loaded_device = Device.find_by_attribute("managed_by_user_id", "two@mci.edu")
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")

    devices = Device.find_all()
    print("All devices:")
    for device in devices:
        print(device)

    