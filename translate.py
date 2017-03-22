"""
TO-DO
"""
# from ioc_writer import ioc_api
from ioc import *

# ID format for translated STIX items
STIX_ID_FMT = 'stix:item-%s'

# Map of CybOX operators to IndicatorItem conditions
CONDITIONS = {
    'Equals': 'is',
    'DoesNotEqual': 'isnot',
    'Contains': 'contains',
    'DoesNotContain': 'containsnot',
}


def create_ioc_object(items, description):
    """TO-DO
    """
    ioc = make_ioc_root()
    ioc.append(make_description_node(description))
    ioc.append(make_author_node())
    ioc.append(make_author_date())
    top_level_or_node = make_indicator_node('OR')
    for i in items:
        node = create_node(i)
        if node is not None:
            top_level_or_node.append(create_node(i))
    ioc.append(make_definition_node(top_level_or_node))
    return ioc

def create_node(data):
    """Take a dict parsed from STIX.collect_info
    Args:
        dictionary object containing 'class' key
    """
    makefunc = INDICATOR_MAP.get(data['class'], None)
    if makefunc is None:
        return makefunc
    return makefunc(data)

def create_dns(data):
    """TO-DO
    """
    condition = CONDITIONS[data.get('condition', 'Equals')]
    document = 'Network'
    search = 'Network/DNS'
    content_type = 'string'
    content = data.get('domain', None)

    return make_indicatoritem_node(condition,
                                   document,
                                   search,
                                   content_type,
                                   content)

def get_hash_class(hashstr):
    """TO-DO
    """
    assert isinstance(hashstr, str)
    if len(hashstr) == 32:
        return 'FileItem/Md5sum'
    elif len(hashstr) == 40:
        return 'FileItem/Sha1sum'
    elif len(hashstr) == 64:
        return 'FileItem/Sha256sum'
    else:
        return 'FileHashes'

def create_file(data):
    """TO-DO
    """
    condition = CONDITIONS[data.get('condition', 'Equals')]
    document = 'FileItem'
    name_flag = data.get('name', False)
    hash_flag = data.get('hash', False)

    if name_flag and hash_flag:
        node = make_indicator_node('AND')
        node.append(create_file_name(condition, document, data['name']))
        [node.append(create_file_hash(condition, document, h)) for h in data['hash']]
        return node
    elif name_flag:
        return create_file_name(condition, document, data['name'])
    elif hash_flag:
        if len(data['hash']) > 1:
            node = make_indicator_node('OR')
            [node.append(create_file_hash(condition, document, h)) for h in data['hash']]
        elif len(data['hash']) == 1:
            return create_file_hash(condition, document, data['hash'][0])
    else:
        return None


def create_file_name(condition, document, filename):
    """TO-DO
    """
    search = 'FileItem/FileName'
    return make_indicatoritem_node(condition,
                                   document,
                                   search,
                                   'string',
                                   filename)

def create_file_hash(condition, document, filehash):
    """TO-DO
    """
    search = get_hash_class(filehash)
    return make_indicatoritem_node(condition,
                                   document,
                                   search,
                                   'string',
                                   filehash)


def create_addr(data):
    """TO-DO
    """
    condition = CONDITIONS[data.get('condition', 'Equals')]
    document = 'PortItem'
    search = 'PortItem/localIP'
    content_type = 'string'
    content = data.get('address', None)
    return make_indicatoritem_node(condition,
                                   document,
                                   search,
                                   content_type,
                                   content)

INDICATOR_MAP = {
    'FileObjectType': create_file,
    'AddressObjectType': create_addr,
    'DomainNameObjectType': create_dns,
}
