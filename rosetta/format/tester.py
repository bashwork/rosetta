from rosetta.core.fields import *
from rosetta.core.message import Message
from rosetta.format.base import Deserializer

class ExampleMessage(Message):
    name = StringField(size=20)
    age  = IntField(size=5)

    class Meta:
        encoded_name = 'ExampleMessage'

class ExampleDeserializer(Deserializer):

    def decode_packet(self, info, packet):
        return packet


packet = {'name':'galen', 'age':'24'}
message = ExampleMessage()
decoder = ExampleDeserializer()
decoder._decode(message, packet)
print message.name, message.age
