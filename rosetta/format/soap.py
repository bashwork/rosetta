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
import yaml

class SoapSerializer:
    '''
    This class allows one to convert to and from
    a message in an object representation and a
    yaml string.
    '''
    
    @staticmethod
    def serialize(input):
        ''' Convert a type to yaml text
        :param input: The type do serialize
        :return: The input serialized to yaml
        '''
        handle = input.__class__
        data   = input.__dict__
        name   = '%s//%s' % (handle.__module__, handle.__name__)
        result = {'name':name, 'data':data}
        return yaml.dump(result)

    @staticmethod
    def deserialize(input):
        ''' Convert serialized yaml back to a type
        :param input: The serialized yaml string
        :return: The initialized type
        '''
        result = yaml.load(input)
        module, type = result['name'].split('//')
        handle = _create(module, type)
        handle.__dict__ = result['data']
        return handle

