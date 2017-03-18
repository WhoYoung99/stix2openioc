import uuid
from lxml import etree as ET

NSMAP = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
         'xsd': 'http://www.w3.org/2001/XMLSchema', }

def create_uuid():
    """Create unique ID for items
    """
    return str(uuid.uuid4())

def make_ioc_root(iocid=None):
    """TODO
    """
    root = ET.Element('ioc', nsmap=NSMAP)
    root.attrib['xmlns'] = 'http://schemas.mandiant.com/2010/ioc'
    if iocid:
        root.attrib['id'] = iocid
    else:
        root.attrib['id'] = create_uuid()
    return root

root = make_ioc_root()
print(root.attrib)