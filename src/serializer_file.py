from datetime import datetime, date, time
from tinydb.storages import JSONStorage
from tinydb_serialization import Serializer, SerializationMiddleware
from datetime import timedelta

#from tinydb_serialization import DateTimeSerializer

class DateSerializer(Serializer):
    # The class this serializer handles --> must be date instead of datetime.date
    OBJ_CLASS = date

    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return date.fromisoformat(s)

class TimeSerializer(Serializer):
    # The class this serializer handles --> must be time instead of datetime.time
    OBJ_CLASS = time
    
    def encode(self, obj):
        return obj.isoformat()

    def decode(self, s):
        return time.fromisoformat(s)
    

class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')
    
    class TimedeltaSerializer(Serializer):
        OBJ_CLASS = timedelta  # The class this serializer handles

        def encode(self, obj):
            return obj.total_seconds()

        def decode(self, s):
            return timedelta(seconds=s)

serializer = SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(), 'TinyDateTime')
serializer.register_serializer(DateSerializer(), 'TinyDate')
serializer.register_serializer(TimeSerializer(), 'TinyTime')