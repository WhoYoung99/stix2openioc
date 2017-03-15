

def ns_tag(ns, name):
    return "{%s}%s" % (ns, name)

def get_description(root):
    '''
    to-do
    '''
    xpath = "./stix:STIX_Header/stix:Description"
    descrip_obj = root.xpath(xpath, namespaces=root.nsmap)
    if descrip_obj == []:
        return None
    return descrip_obj[0].text

def get_indicators(root):
    '''
    to-do
    '''
    xpath = "./stix:Indicators/stix:Indicator"
    return list(root.xpath(xpath, namespaces=root.nsmap))

def get_title(item):
    '''
    to-do
    '''
    tag = ns_tag(item.nsmap['indicator'], 'Title')
    return item.findtext(tag)

def get_type(item):
    '''
    to-do
    '''
    tag = ns_tag(item.nsmap['indicator'], 'Type')
    return item.findtext(tag)

def get_hash(fileobj):
    '''
    to-do
    '''
    tag = ns_tag(fileobj.nsmap['cyboxCommon'], 'Hash')
    item = fileobj.findall(tag)[0]
    tag = ns_tag(fileobj.nsmap['cyboxCommon'], 'Type')
    item = item.find(tag)
    print(item.text, item.getnext().text)


def get_value(item):
    '''
    to-do
    '''
    tag = ns_tag(item.nsmap['indicator'], 'Observable')
    item = item.find(tag)
    tag = ns_tag(item.nsmap['cybox'], 'Object')
    item = item.find(tag)
    tag = ns_tag(item.nsmap['cybox'], 'Properties')
    obser_obj = item.find(tag).getchildren()[0]

    fileobj = obser_obj.getnext()
    if fileobj is not None:
        get_hash(fileobj)
    properties = tuple([obser_obj.text, obser_obj.prefix,
                        obser_obj.keys(), obser_obj.values()])
    return properties