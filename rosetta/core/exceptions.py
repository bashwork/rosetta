'''
Rosetta Exceptions
-------------------

We define all the exceptions used throughout the library here.
For ease of capturing this library's exceptions, all the exceptions
will be sub-classed from RosettaException(Exception).

'''

class RosettaException(Exception):
    '''
    Base exception for the rosetta library
    '''
    pass

class NotImplementedException(RosettaException):
    '''
    Raised when attempting to call a method that has
    not been implemented.  Usually in the case of a
    abstract base class or a work in progress.
    '''
    pass

class ConfigurationException(RosettaException):
    '''
    Raised when attempting to call a method that has
    not been implemented.  Usually in the case of a
    abstract base class or a work in progress.
    '''
    pass

class FieldDoesNotExist(RosettaException):
    '''
    Raised when attempting to reference a field that
    does not exist on the current message
    '''
    pass
