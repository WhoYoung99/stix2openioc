# build-in library
import os
from lxml import etree, objectify

# internal
from stix import *

filename = os.path.join('STIX', 'Stix_xml_33.xml')
tree = etree.parse(open(filename))
root = tree.getroot()
# print(get_description(root))


indicators = get_indicators(root)
for i in indicators:
    print(get_value(i))
    # break

