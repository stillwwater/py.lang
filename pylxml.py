"""
--- pylxml.py ---

compiles .lang files to xml
"""

import pyl
import os
import dicttoxml

from xml.dom.minidom import parseString


def compile(data):
    output = data['__config__']['output']
    os.chdir(output)
    print('working directory: %s' % output)

    for tag in data:
        if tag.startswith('__') and tag.endswith('__'):
            continue
        with open(tag + '.xml', 'w+') as f:
            print('writting to %s' % tag + '.xml...')
            xml = dicttoxml.dicttoxml(data[tag], attr_type=False, custom_root=tag)
            f.write(parseString(xml).toprettyxml())


def main():
    print(__doc__)
    compile(pyl.pyl())

if __name__ == '__main__':
    main()
