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
from lxml import etree

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

