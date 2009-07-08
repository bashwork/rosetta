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
import simplejson

class JsonSerializer:
    '''
    This class contains utilities that allow one to
    quickly serialize and deserialize an object to
    and from json.
    '''
    
    @staticmethod
    def serialize(input):
        ''' Convert a type to json text
        :param input: The type do serialize
        :return: The input serialized to json
        '''
        handle = input.__class__
        data   = input.__dict__
        name   = '%s//%s' % (handle.__module__, handle.__name__)
        result = {'name':name, 'data':data}
        return simplejson.dumps(result)

    @staticmethod
    def deserialize(input):
        ''' Convert serialized json back to a type
        :param input: The serialized json string
        :return: The initialized type
        '''
        result = simplejson.loads(input)
        module, type = result['name'].split('//')
        handle = _create(module, type)
        handle.__dict__ = result['data']
        return handle

