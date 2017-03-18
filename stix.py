# Copyright (c) 2017, Trend Micro Corporation. All right reserved.
# author: whoyoung99@gmail.com
"""
Modeul to parse observables and indicators from STIX and CybOX.
"""

def ns_tag(ns, name):
    """to-do
    """
    return "{%s}%s" % (ns, name)

def get_tag_name(tag):
    """Return only tag value without namespace
    Args:
        tag = {http://cybox.mitre.org/objects#FileObject-2}File_Name
    Return: File_Name
    """
    return str(tag).split('}')[1]

def get_description(root):
    """This will return STIX file's description, not Indicator item's description.
    If you need to get Indicator's description, check "get_indi_descrip"
    """
    xpath = "./stix:STIX_Header/stix:Description"
    descrip_obj = root.xpath(xpath, namespaces=root.nsmap)
    if descrip_obj == []:
        return None
    return descrip_obj[0].text

def get_indicators(root):
    """to-do
    """
    xpath = "./stix:Indicators/stix:Indicator"
    return list(root.xpath(xpath, namespaces=root.nsmap))

def get_indi_title(item):
    """to-do
    """
    tag = ns_tag(item.nsmap['indicator'], 'Title')
    return item.findtext(tag)

def get_indi_type(item):
    """to-do
    """
    tag = ns_tag(item.nsmap['indicator'], 'Type')
    return item.findtext(tag)

def get_indi_descrip(item):
    """to-do
    """
    tag = ns_tag(item.nsmap['indicator'], 'Description')
    descrip = item.findtext(tag)
    if descrip == [] or descrip == '':
        return None
    return descrip

def get_properties_obj(item):
    """Get xsi:type value under cybox:Properties
    """
    xpath = './indicator:Observable\
              /cybox:Object\
              /cybox:Properties'
    pro_obj = item.xpath(xpath, namespaces=item.nsmap)
    if pro_obj == [] or len(pro_obj) > 1:
        return None
    return pro_obj[0]

def get_properties_attr(obj):
    """to-do
    """
    tag = ns_tag(obj.nsmap['xsi'], 'type')
    attribute = obj.attrib.get(tag)
    return attribute

def collect_info(item):
    """Return a dict object containing parsed data
    If property attribute is not supported, return empty dict
    """
    obj = get_properties_obj(item)
    attr = get_properties_attr(obj)
    description = get_indi_descrip(item)
    if attr in properties_attrmap:
        makefunc = properties_attrmap[attr]
        content = makefunc(obj)
    else:
        print('Unsupported Object: {}'.format(attr))
        content = {}
    content['class'] = attr
    if description is not None:
        content['description'] = description
    return content

def get_fileobj_data(obj):
    """Parser based on conventional structure of FileObjectType
    Args:
        type(obj) = <Element cybox:Properties>
    Return:
        a dict() object, containing 1. FileName,
                                    2. its corrosponding Conditoin,
                                    3. Hash value
    """
    flag_in_hash_section = False
    data = {}
    # data['class'] = 'FileObj'
    for i in obj.iter():
        tag = get_tag_name(i.tag)
        if tag == 'File_Name':
            data['name'] = i.text
            data.update(i.attrib)
        elif tag == 'Hashes':
            flag_in_hash_section = True
        if flag_in_hash_section and tag == 'Simple_Hash_Value':
            hashvalue = i.text
            if data.get('hash', None) is None:
                data['hash'] = [hashvalue,]
            else:
                data['hash'].append(hashvalue)
            flag_in_hash_section = False
    return data

def get_addrobj_data(obj):
    """Parser based on conventional structure of AddressObjectType
    to-do
    """
    data = {}
    # data['class'] = 'AddressObj'
    for i in obj.iter():
        tag = get_tag_name(i.tag)
        if tag == 'Address_Value':
            data.update(i.attrib)
            data['address'] = i.text
    return data


def get_domainobj_data(obj):
    """Parser based on conventional structure of DomainNameObjectType
    to-do
    """
    data = {}
    # data['class'] = 'DomainNameObj'
    for i in obj.iter():
        tag = get_tag_name(i.tag)
        if tag == 'Value':
            data.update(i.attrib)
            data['domain'] = i.text
    return data

properties_attrmap = {
    'DomainNameObj:DomainNameObjectType': get_domainobj_data,
    'FileObj:FileObjectType': get_fileobj_data,
    'AddressObj:AddressObjectType': get_addrobj_data,
}
