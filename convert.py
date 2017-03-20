# build-in library
import os
import sys
from lxml import etree

# external library
# from ioc_writer import ioc_api

# internal library
from ioc import *
from stix import *
from translate import *

filename = 'Stix_xml_33.xml'
filepath = os.path.join('STIX', filename)
tree = etree.parse(open(filepath))
root = tree.getroot()
description = get_description(root)

# Parsing STIX file
indicators = get_indicators(root)
items = [collect_info(i) for i in indicators]
# for i in indicators:
#     data = collect_info(i)
#     print(data)

# Writing OpenIOC file
ioc = create_ioc_object(items, filename, description)
ioc.write_ioc_to_file('STIX')
# sys.exit(0)
