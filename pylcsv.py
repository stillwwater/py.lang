"""
--- pylcsv.py ---

compiles .lang files to csv
"""

import pyl
import os


class PylCSV:

    def __init__(self, data: dict):
        self.data = data

    def to_csv(self):
        os.chdir(self.data['__config__']['output'])
        print('working directory: %s' % self.data['__config__']['output'])

        for key in self.data:
            if key.startswith('__') and key.endswith('__'):
                continue

            self.write_file(key, self.get_head())

    def write_file(self, tag: str, head: str):
        try:
            os.remove(tag + '.csv')
        except OSError:
            pass
        with open(tag + '.csv', 'a') as f:
            print('writting to %s' % tag + '.csv...')
            f.write(head)
            for key in self.data[tag]:
                buffer = ''
                for lang in self.data[tag][key]:
                    print('[%s] buffering "%s" (%s)' % (tag, key, lang))
                    buffer += self.data[tag][key][lang] + ','
                f.write('%s,%s\n' % (key, buffer[:-1]))

    def get_head(self):
        head = 'Key,'

        if (isinstance(self.data['__head__']['lang'], list)):
            head += ','.join(self.data['__head__']['lang'])
        else:
            head += self.data['__head__']['lang']

        return head + '\n'


def main():
    print(__doc__)
    csv = PylCSV(pyl.pyl())
    csv.to_csv()
    print('\ndone.\n')

if __name__ == '__main__':
    main()
