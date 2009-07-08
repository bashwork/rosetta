'''
Packet Field Meta Objects
--------------------------

The field classes will be used to describe data fields in
a message. By simply assigning a property a field object
and filling in the neccessary properties, one can create a
protocol independent message format that can be serialized
and deserialized to and from any format. The following is 
an example of the intended useage::

    class Example(Message):
        broker   = StringField(size=8, name='Broker')
        count    = IntField(size=4,    name='Count')
        symbol   = StringField(size=4, name='Symbol')
        flag     = BoolField(name='Symbol')
        type     = StringField(size=4, name='Type', const=True, value='AON')

Types
--------------------------

Instead of creating a generic field and having to pass the type
each time, we create base classes that set the type for us. So::

    StringField(Field):
        def __init__(self, *args, **kwargs):
            self.type = str

For the value of the type we require a type object that can convert
an encoded type (usually a string) back to the given type.
For the main types (string, int, bool, etc) we simply use the python
types.  In the future we may need more complicated functors (Date,
Enumeration, Time, etc)::

    class NewType(type):

        def __call__(self, value):

    NewTypeField(Field):
        def __init__(self, *args, **kwargs):
            self.type = 

Const
--------------------------

By setting the const field to true, the current value will be unable
to be changed. This is useful for things like message IDs, message
sentinals, or version numbers.

Optional
--------------------------

By setting the optional flag to true, the field will not be encoded
unless it's value has changed from the default value.

Repeat
--------------------------

By setting the repeat field to true, the value can be set to a list
of values instead of a single value and will be treated as multiple
fields of the same type.

.. todo::

   Possible fields we need to add are choice, enumeration, bit-field.
'''
from rosetta.core.exceptions import FieldDoesNotExist

#---------------------------------------------------------------------------# 
# Logger
#---------------------------------------------------------------------------# 
import logging
_logger = logging.getLogger('rosetta.core.fields')

#--------------------------------------------------------------------------------#
# Helper Classes
#--------------------------------------------------------------------------------#
class NOT_PROVIDED:
    ''' Class used to flag invalid values '''
    pass

#--------------------------------------------------------------------------------#
# Base Field
#--------------------------------------------------------------------------------#

class Field(object):
    '''
    :param type: The type of this field, currently we use python types
    :param size: The encoded size of the field (if applicable)
    :param name: The field name used to reference by (in python)
    :param verbose_name: The field name used for pprinting
    :param encoded_name: The field name used for message name (default to name)
    :param value: The current value of the field
    :param default: The default value of the field
    :param const: True if this value cannot be changed
    :param optional: True if this field is optional
    '''
    _order_counter = 0

    def __init__(self, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        self.type         = kwargs.get('type', str)
        self.size         = kwargs.get('size', 0)
        self.default      = kwargs.get('default', NOT_PROVIDED)
        self.const        = kwargs.get('const', False)
        self.optional     = kwargs.get('optional', False)
        self.repeated     = kwargs.get('repeated', False)
        self.name         = kwargs.get('name', '')
        self.verbose_name = kwargs.get('verbose_name', self.name)
        self.encoded_name = kwargs.get('encoded_name', self.name)

        if 'value' in kwargs.keys():
            self.value = kwargs.get('value')
        elif self.default is not NOT_PROVIDED:
            self.value = self.default
        else: self.value = None

        # used to preserve order of Fields
        self.order = Field._order_counter
        Field._order_counter += 1

    def __cmp__(self, other):
        ''' Compare fields based on order
        :param other: The field to be compared to
        '''
        return cmp(self.order, other.order)

    def __str__(self):
        ''' Return a string version of the field value
        :return: The field value is string form
        '''
        return str(self.value)

    def is_required(self):
        ''' Check if this is a required field
        :return: True if it is, False otherwise
        '''
        return True if not self.optional else self.value != self.default

    def has_default(self):
        ''' Check if we have a default value
        :return: True if we do, False otherwise
        '''
        return self.default is not NOT_PROVIDED

    def get_default(self):
        ''' Gets the default value for this field
        :return: The default value if it exists, or None
        '''
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return None

    def set_attributes_from_name(self, name):
        ''' Sets the various names from the field name
        :param name: The message level field name

        If the verbose and encoded names have already been
        set from the field initializer, they are not reset.
        If they have not, we build them from the message level
        field name.
        '''
        self.name = name
        if not self.verbose_name and name:
            self.verbose_name = name.replace('_', ' ')
        if not self.encoded_name and name:
            self.encoded_name = name.replace('_', '')

    def contribute_to_class(self, cls, name):
        ''' Helper method to add this to the underlying class
        :param cls: The holding class
        '''
        self.set_attributes_from_name(name)
        cls._meta.add_field(self)

#--------------------------------------------------------------------------------#
# Field Types
#--------------------------------------------------------------------------------#
         
class PaddingField(Field):
    ''' Packet Field representing buffer padding
    '''
    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['type']    = str
        kwargs['value']   = ' '
        kwargs['const']   = True
        kwargs['default'] = ' '
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'padding'

class StringField(Field):
    ''' Packet Field representing a c string
    '''
    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['default'] = ''
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'string'

class CharField(Field):
    ''' Packet Field representing a single character
    '''
    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['type']    = str
        kwargs['size']    = 1   # can never be more than a byte
        kwargs['default'] = ' '
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'character'

class IntField(Field):
    ''' Packet Field representing an integar
    '''
    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['type']    = int
        kwargs['default'] = 0
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'integar'

class BoolField(Field):
    ''' Packet Field representing a boolean
    '''
    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['type']    = bool
        kwargs['size']    = 1   # can never be more than a byte
        kwargs['default'] = False
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'bool'

class FloatField(Field):
    ''' Packet Field representing a float
    '''
    def __init__(self, precision=2, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        self.precision    = precision
        kwargs['type']    = float
        kwargs['default'] = 0.0
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'float'

class DecimalField(Field):
    ''' Packet Field representing a decimal
    '''
    def __init__(self, precision=2, *args, **kwargs):
        ''' Initialize a new instance of the Field
        '''
        kwargs['type']    = decimal.Decimal
        kwargs['default'] = '0.0'
        Field.__init__(self, *args, **kwargs)

    def get_type_name(self):
        ''' Return a readable type name
        :return: The type name
        '''
        return 'decimal'

