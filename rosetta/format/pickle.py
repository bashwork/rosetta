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
try: # try to import faster pickle first
    import cPickle as pickle
except:
    import pickle

class PickleSerializer:
    '''
    This class allows one to convert to and from
    a message in an object representation and a
    pickle string.
    '''
    
    @staticmethod
    def serialize(input):
        ''' Convert a type to pickle text
        :param input: The type do serialize
        :return: The input serialized to pickle
        '''
        try:
            return pickle.dumps(input)
        except pickle.PickleError: return None

    @staticmethod
    def deserialize(input):
        ''' Convert serialized pickle back to a type
        :param input: The serialized pickle string
        :return: The initialized type
        '''
        try:
            return pickle.loads(input)
        except pickle.PickleError: return None

