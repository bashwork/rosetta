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

class Encoder(object):
    '''
    Base class for a serializer object
    '''

    def __init__(self):
        ''' Initializes a new instance
        '''
        pass

    def _encode(self, message):
        ''' Serialize a given object to a data stream
        :param input: The object to serialize
        :return: The resulting data stream

        This is a bit risky and really not all that great of design
        '''
        description = self._create_information(message)
        message  = ''
        message += self.build_header(description)
        message += self.bulid_fields(message.fields)
        message += self.build_trailer(description)
        return message

    def _create_information(self, message):
        ''' A simple factory to supply the format builder what it needs
        The idea is that we don't want to send the format builder the
        underlying message instance, so instead, we send them the pertinant
        information.

        ToDo, implement this in the message and cache?
        '''
        result = {}
        result['size'] = message._message_size()
        result['name'] = message._meta.encoded_name
        result['field_count'] = len(message._meta.fields)
        return result

    def build_header(self, message):
        ''' Build the message header
        :param message: The message object with metadata
        :return: The fully built message header
        '''
        return ''

    def build_body(self, fields):
        ''' Build the message stream from the fields
        '''
        raise NotImplementedException()

    def build_footer(self, message):
        ''' Build the message footer
        :param message: The message object with metadata
        :return: The fully built message trailer
        '''
        return ''
        
 
class Decoder(object):
    '''
    Base class for a deserializer object
    '''

    def __init__(self):
        pass

    def _decode(self, message, packet):
        ''' Deserialize a given object to a data stream
        :param message: The message to decode to
        :param packet: The raw packet data
        :return: The resulting data stream
        '''
        description = self._create_information(message)
        decode = self.decode_packet(description, packet)
        fields = message._meta.get_all_field_names()
        for key,value in decode.iteritems():
            if key in fields:
                setattr(message, key, value)
            # log bad field ?

    def decode_packet(self, info, packet):
        ''' Decode the packet data back into fields
        :param info: Message type information
        :param packet: The raw packet to decode
        '''
        raise NotImplementedException()

    def _create_information(self, message):
        ''' A simple factory to supply the format builder what it needs
        The idea is that we don't want to send the format builder the
        underlying message instance, so instead, we send them the pertinant
        information.

        ToDo, implement this in the message and cache?
        '''
        result = {}
        result['size'] = message._message_size()
        result['name'] = message._meta.encoded_name
        result['field_count'] = len(message._meta.fields)
        return result

    #def create(module, type):
    #    ''' Dynamically import a type
    #    :param module: The module to import
    #    :param type: The type to create
    #    '''
    #    short = module
    #    local = locals()
    #    if '.' in module:
    #        short = module.split('.', 1)[0]
    #    local[short] = __import__(short)
    #    return eval('%s.%s()' % (module, type))

