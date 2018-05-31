"""
--- pyljson.py ---

compiles .lang files to json
"""

import pyl
import os
import json


def compile(data):
    output = data['__config__']['output']
    os.chdir(output)
    print('working directory: %s' % output)

    for tag in data:
        if tag.startswith('__') and tag.endswith('__'):
            continue
        with open(tag + '.json', 'w+') as f:
            print('writting to %s' % tag + '.json...')
            f.write(json.dumps({tag: data[tag]}, indent=4, sort_keys=True))


def main():
    print(__doc__)
    compile(pyl.pyl())

if __name__ == '__main__':
    main()
