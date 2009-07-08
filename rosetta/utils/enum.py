'''
'''

class Enum(object):
    ''' Enumerated type for python
    '''
    __readonly = False

    def __init__(self, *args, **kwargs):
        ''' Initialize a new instance of the type
        '''
        self.__count  = 0
        self._fields = {}

        for key, val in kwargs.iteritems():
            self._add_enum(key, val)
        for key in args:
            self._add_enum(key)

        self.__readonly = True

    def _add_enum(self, value, index=-1):
        count = index
        if count == -1:
            count = self.__count
            self.__count += 1
        self._fields[value] = count 
        setattr(self, value, count)

    def _exception(self):
        ''' Helper to apply an exception
        :param args: Arguments to apply to the exception
        '''
        raise AttributeError('Cannot Modify Enumeration')

    def _lookup(self, index):
        if isinstance(index, str):
            return self._fields[index]
        else:
            for k,v in self._fields.iteritems():
                if index == v: return k
        raise KeyError

    #-----------------------------------------------------------------------# 
    # The Candy
    #-----------------------------------------------------------------------# 
    def __setattr__(self, key, value):
        ''' Helper to block writing to the fields
        '''
        if self.__readonly:
            self._exception()
        super(Enum, self).__setattr__(key, value)

    __delattr__ = lambda s, i: s._exception()
    __delitem__ = lambda s, i: s._exception()
    __setitem__ = lambda s, k, v: s._exception()
    __getitem__ = lambda s, k: s._lookup(k)
    __call__    = lambda s, k: s._lookup(k)
    __len__     = lambda s: len(s._fields)
    __iter__    = lambda s: iter(s._fields)

