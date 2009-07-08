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
import cPickle as pickle
import simplejson
import yaml
from lxml import etree

#--------------------------------------------------------------------------------#
# Helpers
#--------------------------------------------------------------------------------#
def _create(module, type):
    ''' Dynamically import a type
    :param module: The module to import
    :param type: The type to create
    '''
    short = module
    local = locals()
    if '.' in module:
        short = module.split('.', 1)[0]
    local[short] = __import__(short)
    return eval('%s.%s()' % (module, type))
 
#--------------------------------------------------------------------------------#
# Serializers 
#--------------------------------------------------------------------------------#

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

class AsciiSerializer:
    '''
    This class allows one to convert to and from
    a message in an object representation and an
    order server binary packet.

    We actually cannot do this effectively without
    metadata stored for each field.
    '''

    @staticmethod
    def serialize(input):
        ''' Convert a type to XML text
        :param input: The type do serialize
        :return: The input serialized to xml
        '''
        data = input.__dict__
        pass

    @staticmethod
    def deserialize(input):
        ''' Convert serialized XML back to a type
        :param input: The serialized XML string
        :return: The initialized type
        '''
        pass

class BinarySerializer:
    '''
    This class allows one to convert to and from
    a message in an object representation and an
    order server binary packet.

    We actually cannot do this effectively without
    metadata stored for each string field.
    '''
    
    @staticmethod
    def serialize(input):
        ''' Convert a type to XML text
        :param input: The type do serialize
        :return: The input serialized to xml
        '''
        data = input.__dict__
        pass

    @staticmethod
    def deserialize(input):
        ''' Convert serialized XML back to a type
        :param input: The serialized XML string
        :return: The initialized type
        '''
        pass

class XmlSerializer:
    '''
    This class allows one to convert to and from
    a message in an object representation and a
    xml string.
    '''
    
    @staticmethod
    def serialize(input):
        ''' Convert a type to XML text
        :param input: The type do serialize
        :return: The input serialized to xml
        '''
        data = input.__dict__
        name = input.__class__.__name__
        mod  = input.__class__.__module__

        root = etree.Element(name, module=mod)
        for value in data.iteritems():
            node = etree.SubElement(root, value[0],
                type=type(value[1]).__name__)
            node.text = "%s" % value[1]
        return etree.tostring(root, xml_declaration=True)

    @staticmethod
    def deserialize(input):
        ''' Convert serialized XML back to a type
        :param input: The serialized XML string
        :return: The initialized type
        '''
        root   = etree.fromstring(input)
        handle = _create(root.attrib['module'], root.tag)
        result = {}
        for child in root.iterchildren():
            result[child.tag] = eval('%s("%s")' %
                (child.attrib['type'], child.text))
        handle.__dict__ = result
        return handle

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

class YamlSerializer:
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

#---------------------------------------------------------------------------# 
# Exported symbols
#---------------------------------------------------------------------------# 
__all__ = [
    "JsonSerializer",
    "XmlSerializer",
    "AsciiSerializer",
    "BinarySerializer",
    "PickleSerializer",
    "YamlSerializer",
]

