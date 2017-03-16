# build-in library
import os
from lxml import etree

# external library
from ioc_writer import ioc_api

# internal library
from stix import *

filename = os.path.join('STIX', 'Stix_xml_36.xml')
tree = etree.parse(open(filename))
root = tree.getroot()
print(get_description(root))

# Parsing STIX file
indicators = get_indicators(root)
for i in indicators:
    print(collect_info(i))

# Writing OpenIOC file

