import uuid
import os
import sys
import datetime
from lxml import etree as ET

NSMAP = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
         'xsd': 'http://www.w3.org/2001/XMLSchema', }

VALID_INDICATOR_OPERATORS = ['AND', 'OR']

def create_uuid():
    """Create unique ID for items
    """
    return str(uuid.uuid4())

def get_current_date():
    """TODO
    """
    time = datetime.datetime.utcnow()
    timestring = time.strftime('%Y-%m-%dT%H:%M:%S')
    return timestring

def set_root_lastmodified(_root, date=None):
    """TODO
    """
    if date:
        _root.attrib['last-modified'] = date
    else:
        _root.attrib['last-modified'] = get_current_date()

def make_ioc_root(iocid=None):
    """TODO
    """
    root_node = ET.Element('ioc', nsmap=NSMAP)
    root_node.attrib['xmlns'] = 'http://schemas.mandiant.com/2010/ioc'
    if iocid:
        root_node.attrib['id'] = iocid
    else:
        root_node.attrib['id'] = create_uuid()
    root_node.attrib['last-modified'] = get_current_date()
    return root_node

def make_description_node(description):
    """TODO
    """
    node = ET.Element('short_description')
    node.text = description
    return node

def make_author_node(author='Trend Micro STIX-converter'):
    """TODO
    """
    node = ET.Element('authored_by')
    node.text = author
    return node

def write_ioc_to_file(root, output_dir=None, force=False):
    """
    Serialize an IOC, as defined by a set of etree Elements, to a .IOC file.
    :param root: etree Element to write out.  Should have the tag 'OpenIOC'
    :param output_dir: Directory to write the ioc out to.  default is current working directory.
    :param force: If set, skip the root node tag check.
    :return: True, unless an error occurs while writing the IOC.
    """
    root_tag = 'ioc'
    if not force and root.tag != root_tag:
        raise ValueError('Root tag is not "{}".'.format(root_tag))
    default_encoding = 'utf-8'
    tree = root.getroottree()
    # noinspection PyBroadException
    try:
        encoding = tree.docinfo.encoding
    except:
        log.debug('Failed to get encoding from docinfo')
        encoding = default_encoding
    ioc_id = root.attrib['id']
    fn = ioc_id + '.ioc'
    if output_dir:
        fn = os.path.join(output_dir, fn)
    else:
        fn = os.path.join(os.getcwd(), fn)
    try:
        with open(fn, 'wb') as fout:
            fout.write(ET.tostring(tree,
                                   encoding=encoding,
                                   xml_declaration=True,
                                   pretty_print=True))
    except (IOError, OSError):
        return False
    except:
        raise
    return True

def make_indicator_node(operator, nid=None):
    """
    This makes a Indicator node element.  These allow the
    construction of a logic tree within the IOC.
    :param operator: String 'AND' or 'OR'.
     The constants ioc_api.OR and ioc_api.AND may be used as well.
    :param nid: This is used to provide a GUID for the Indicator.
     The ID should NOT be specified under normal circumstances.
    :return: elementTree element
    """
    if operator.upper() not in VALID_INDICATOR_OPERATORS:
        raise ValueError('Indicator operator must be in [{}].'.format(VALID_INDICATOR_OPERATORS))
    i_node = ET.Element('Indicator')
    if nid:
        i_node.attrib['id'] = nid
    else:
        i_node.attrib['id'] = create_uuid()
    i_node.attrib['operator'] = operator.upper()
    return i_node

def make_indicatoritem_node(condition,
                            document,
                            search,
                            content_type,
                            content,
                            context_type='mir',
                            nid=None):
    """
    This makes a IndicatorItem element.  This contains the actual threat intelligence in the IOC.
    :param condition: This is the condition of the item ('is', 'contains', 'matches', etc). The following contants in ioc_api may be used:
==================== =====================================================
Constant             Meaning
==================== =====================================================
ioc_api.IS           Exact String match.
ioc_api.CONTAINS     Substring match.
ioc_api.MATCHES      Regex match.
ioc_api.STARTS_WITH  String match at the beginning of a string.
ioc_api.ENDS_WITH    String match at the end of a string.
ioc_api.GREATER_THAN Integer match indicating a greater than (>) operation.
ioc_api.LESS_THAN    Integer match indicator a less than (<) operation.
==================== =====================================================
    :param document: Denotes the type of document to look for the encoded artifact in.
    :param search: Specifies what attribute of the document type the encoded value is.
    :param content_type: This is the display type of the item. This is normally derived from the iocterm for the search value.
    :param content: The threat intelligence that is being encoded.
    :param preserve_case: Specifiy that the content should be treated in a case sensitive manner.
    :param negate: Specifify that the condition is negated. An example of this is:
       @condition = 'is' & @negate = 'true' would be equal to the
       @condition = 'isnot' in OpenIOC 1.0.
    :param context_type: Gives context to the document/search information.
    :param nid: This is used to provide a GUID for the IndicatorItem. The ID should NOT be specified under normal
     circumstances.
    :return: an elementTree Element item
    """
    # validate condition
    if condition not in VALID_INDICATORITEM_CONDITIONS:
        raise ValueError('Invalid IndicatorItem condition [{}]'.format(condition))
    ii_node = ET.Element('IndicatorItem')
    if nid:
        ii_node.attrib['id'] = nid
    else:
        ii_node.attrib['id'] = create_uuid()
    ii_node.attrib['condition'] = condition
    
    context_node = ioc_et.make_context_node(document, search, context_type)
    content_node = ioc_et.make_content_node(content_type, content)
    ii_node.append(context_node)
    ii_node.append(content_node)
    return ii_node

root = make_ioc_root()
root.append(make_description_node('Some description about the IOC.'))
root.append(make_author_node())
sys.exit(write_ioc_to_file(root, output_dir=None, force=False))
