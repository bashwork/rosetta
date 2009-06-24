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

..:todo: Maybe an enumeration field
'''

#--------------------------------------------------------------------------------#
# Helper Classes
#--------------------------------------------------------------------------------#
class NOT_PROVIDED:
    ''' Class used to flag invalid values '''
    pass

class FieldDoesNotExist(Exception):
    '''
    Raised when attempting to reference a field that
    does not exist on the current message
    '''
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

#--------------------------------------------------------------------------------#
# Exported Symbols
#--------------------------------------------------------------------------------#
__all__ = [
    'PaddingField', 'StringField', 'CharField', 'IntField',
    'BoolField', 'FloatField', 'DecimalField',
]
