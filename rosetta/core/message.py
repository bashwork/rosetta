'''
Message Base Classes
--------------------------

This is the magical base class that all messages should derive
from. Bascially, it sets up the message correctly so that:

- The fields are protected and abstracted
- The meta structures (used for (de)serialization works
- and more!

..:todo: Add support for inheritence

For this we will need the idea of an abstract message as well as means
of finding the parent chain and retrieving fields from them as well.
'''
try:
    set
except NameError:
    from sets import Set as set # Python 2.3 fallback.

from rosetta.core.options import Options

#---------------------------------------------------------------------------# 
# Logger
#---------------------------------------------------------------------------# 
import logging
_logger = logging.getLogger('rosetta.core.message')

class MessageBase(type):
    ''' Metaclass use to build a message

    This constructs a Message by going through its attributes and initializing
    it with the various fields and Meta values.
    '''

    def __new__(cls, name, bases, attrs):
        ''' Creates a new instance of message
        :param cls: The class to instantiate
        :param name: The class name
        :param bases: The subclasses of the class
        :param attrs: The class attributes
        '''
        # if not a subclass of message, simply instantiate
        super_new = super(MessageBase, cls).__new__
        parents = [base for base in bases if isinstance(base, MessageBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})

        # extract current Meta information
        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else: meta = attr_meta
        new_class.add_to_class('_meta', Options(meta))

        # bail out early if we have already created this class.
        #m = get_model(new_class._meta.app_label, name, False)
        #if m is not None:
        #    return m

        # add all fields to the class.
        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        return new_class

    def add_to_class(cls, name, value):
        ''' Helper to facilitate where attributes are added
        :parm name: The name of the attribute to add
        :param value: The value of the attribute to add

        If the value we are assigning has a 'contribute_to_class' method
        defined, we assume it needs to add itself in a special way, so we
        use its method. Otherwise, we simply set it as an attribute.
        '''
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else: setattr(cls, name, value)

class Message(object):
    ''' ...documentation...
    '''
    __metaclass__ = MessageBase

    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance

        Django loops through the args and kwargs and izips
        the arguments with the fields (for a copy constructor)
        It then assigns the leftover kwargs to properties.
        '''
        field_iter = iter(self._meta.fields)
        for field in field_iter:
            setattr(self, field.name, field.value)

    def _message_size(self):
        ''' Return the total size of the message
        :return: The total message size in bytes
        '''
        return sum([i.size for i in self._meta.fields])

    def _serialize(self, method):
        ''' Serialize this message object into a message string
        :param method: The method used to serialize the message
        :return: The serialized form of this message
        '''
        return method.serialize(self._meta.fields())

    def _deserialize(self, method, input):
        ''' Decode an input message back into the message object
        :param method: The method used to deserialize the message
        :param input: The message to deserialize
        '''
        method.deserialize(self._meta.fields(), input)

