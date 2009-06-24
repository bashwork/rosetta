'''
Message Options Handler
------------------------

Basically, this is the meta information handler class
for a message.

We should probobly set the groundwork now for doing inheritable
messages, but we need to get the base stuff right first.
'''
from bisect import bisect
from rosetta.fields import FieldDoesNotExist

#--------------------------------------------------------------------------------#
# Allowed Meta Values 
#--------------------------------------------------------------------------------#
DEFAULT_NAMES = (
    'verbose_name', 'encoded_name', 'total_size'
)

class Options(object):

    def __init__(self, meta):
        ''' Initialize a new instance
        :param meta: The base meta object
        '''
        self.local_fields = []
        self.meta = meta

    def contribute_to_class(self, cls, name):
        ''' ...hello...
        :param cls: The class calling down to us
        :param name: The attribute to add
        '''
        cls._meta = self
        self.object_name = cls.__name__
        self.module_name = self.object_name.lower()

        # apply overriden meta values
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs.pop(attr_name))
                elif hasattr(self.meta, attr_name): # I don't know why this is done
                    setattr(self, attr_name, getattr(self.meta, attr_name))

    def add_field(self, field):
        ''' Appends a field to the field collection
        We use the order column to insert the fields in the correct
        order that they were declared as.

        :param field: The field to append to the collection
        '''
        self.local_fields.insert(bisect(self.local_fields, field), field)
        # invalidate the cache
        if hasattr(self, '_name_map'):
            del self._name_map

    def _fields(self):
        ''' Returns the list of fields
        :return: The local handle to the field list
        '''
        # django uses a cache for including parent fields as well
        return self.local_fields

    fields = property(_fields)

    def get_field(self, name):
        ''' Returns the requested field
        :param name: The field name to retrieve
        :return: The requested field or Exception if field does not exist
        '''
        for field in self.fields:
            if field.name == name:
                return field
        raise FieldDoesNotExist('no field named %s' % name)

    def get_field_by_name(self, name):
        ''' Returns a field by its print name.
        :param name: The field to retrieve
        :return: The requested field

        Uses a cache internally, so after the first access, this is very fast.
        '''
        try:
            try:
                return self._name_map[name]
            except AttributeError:
                cache = self.init_name_map()
                return cache[name]
        except KeyError:
            raise FieldDoesNotExist('has no field named %s' % (name))

    def get_all_field_names(self):
        ''' Return a list of all the field print names
        :return: List of all the field names
        '''
        try:
            cache = self._name_map
        except AttributeError:
            cache = self.init_name_map()
        names = cache.keys()
        names.sort()
        return names # django does elimination of internal names starting with +

    def init_name_map(self):
        ''' Initalizes the field print name lookup
        :return: The built name cache
        '''
        pass
