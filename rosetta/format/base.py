'''
Message Serializers
-------------------

Instead of having every message derive from a protocol that
decides how to encode/decode it, we instead are pulling the
relevant code outside of the class.

Since we can introspect each message and we know what our
messages look like, we an serialize from the outside just as
easily from the inside.  This allows us to supply a pluggable
serializer.

In order to create a new serializer, simply supply serialize
and a deserialize static methods that operate on a message and
a serialized message respectively.  Note, the deserialize _must_
be able to reconstuct the given message from the serialize dump!
'''
from rosetta.core.exceptions import NotImplementedException

class Serializer(object):
    '''
    Base class for a serializer object
    '''

    def __init__(self):
        ''' Initializes a new instance
        '''
        pass

    def _build(self, message):
        ''' Serialize a given object to a data stream
        :param input: The object to serialize
        :return: The resulting data stream
        '''
        message = ''
        message += self.build_header(message)
        message += self.bulid_fields(message.fields())
        message += self.build_trailer(message)
        return message

    def build_header(self, message)
        ''' Build the message header
        :param message: The message object with metadata
        :return: The fully built message header
        '''
        return ''

    def build_fields(self, fields)
        ''' Build the message stream from the fields
        '''
        raise NotImplementedException()

    def build_trailer(self, message)
        ''' Build the message trailer
        :param message: The message object with metadata
        :return: The fully built message trailer
        '''
        return ''
        
 
class Deserializer(object):
    '''
    Base class for a deserializer object
    '''

    def __init__(self):
        pass

    def convert(self, input):
        ''' Deserialize a given object to a data stream
        :param input: The object to serialize
        :return: The resulting data stream
        '''
        raise NotImplementedException()

    def create(module, type):
        ''' Dynamically import a type
        :param module: The module to import
        :param type: The type to create
        '''
        short = module
        local = locals()
        if '.' in module:
            short = module.split('.', 1)[0]
        local[short] = __import__(short)
        return eval('%s.%s()' % (module, type))
