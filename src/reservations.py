import os
from tinydb import TinyDB, Query
from serializer_file import serializer

class Reservation():

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'device_manager.json'), storage=serializer).table('reservations')


    def __init__(self, res_device_id : str, res_user_id : str, res_start_date, res_end_date, res_status=None, doc_id=None) -> None:
        self.res_device_id = res_device_id
        self.res_user_id = res_user_id
        self.res_start_date = res_start_date
        self.res_end_date = res_end_date
        self.res_status = res_status
        self.is_active = True
        self.id = doc_id

        print(f"New reservation created: {self.res_device_id} ({self.res_user_id})")

    def __str__(self):
        return f'Reservation (Object) {self.res_device_id} ({self.res_user_id})'
    
    def __repr__(self):
        return self.__str__()
    
    def store_data(self):
        print("Storing data...")
        ReservationQuery = Query()
        result = self.db_connector.search(ReservationQuery.res_device_id == self.res_device_id)
        if result:
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    def delete(self):
        print("Deleting data...")
        ReservationQuery = Query()
        result = self.db_connector.search(ReservationQuery.res_device_id == self.res_device_id)
        if result:
            self.db_connector.remove(doc_ids=[result[0].doc_id])
            print("Data deleted.")
        else:
            print("Data not found.")

    def set_res_user_id(self, res_user_id: str):
        self.res_user_id = res_user_id
        self.store_data()

    @classmethod
    def find_by_attribute(cls, by_attribute : str, attribute_value : str, num_to_return=1):
        ReservationQuery = Query()
        result = cls.db_connector.search(ReservationQuery[by_attribute] == attribute_value)

        if result:
            data = result[:num_to_return]
            reservation_results = [cls.instanciate(d) for d in data]
            return reservation_results if num_to_return > 1 else reservation_results[0]
        else:
            return None
        
    @classmethod
    def find_all(cls) -> list:
        reservations = []
        for reservation_data in Reservation.db_connector.all():
            reservations.append(cls.instanciate(reservation_data))
        return reservations
    @classmethod
    def instanciate(cls, data):
        return cls(data['res_device_id'], data['res_user_id'], data['res_start_date'], data['res_end_date'])
    
if __name__ == '__main__':
    res = Reservation("1", "1", "2021-10-01 12:00", "2021-10-01 13:00")
    res.store_data()
    res.set_res_user_id("2")
    #res.delete()
    print(Reservation.find_all())
    print(Reservation.find_by_attribute('res_device_id', '1'))