# build-in library
import os
import sys
import argparse
import logging
from lxml import etree

# internal library
import ioc
import stix
import translate


def main(options):
    """todo
    """
    loc = os.getcwd()
    filepath = os.path.join(loc, options.src_file)
    try:
        tree = etree.parse(open(filepath))
    except FileNotFoundError as err:
        sys.exit(err)
    root = tree.getroot()
    description = stix.get_description(root)

    indicators = stix.get_indicators(root)
    items = [stix.collect_info(i) for i in indicators]

    nodes = translate.create_ioc_object(items, description)
    print('Output file: %s' % options.src_file)
    outpath = os.getcwd()
    if options.output_dir is not None:
        outpath = os.path.join(outpath, options.output_dir)
    print('Output path: %s' % outpath)
    sys.exit(ioc.write_ioc_to_file(nodes,
                                   options.src_file,
                                   output_dir=options.output_dir,
                                   force=False))


def makeargparser():
    """Parse arguments about target file
    """
    parser = argparse.ArgumentParser(description='Convert a STIX to OpenIOC format.')
    parser.add_argument('-s', '--source', dest='src_file', required=True, type=str,
                        help='source file (.xml, .stix) containing IOC data')
    parser.add_argument('-o', '--output_dir', dest='output_dir', default=None,
                        help='location to write IOC to. default is current working directory')
    return parser


if __name__ == '__main__':
    PARSER = makeargparser()
    OPTS = PARSER.parse_args()
    main(OPTS)
