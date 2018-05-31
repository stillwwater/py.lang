"""
--- pyl parser ---

Parses .lang files to a python dictionary

---

--- config ---
include:
  - ''

output: ''

fallback-tag: out

output-structure: one-lang-per-file

COMMENT: '#'
INDENT: ' '
NEW_LINE: '\n'
OPEN_DEF: ':'
END_DEF: 'end'
OPEN_TAG: '['
CLOSE_TAG: ']'
SEP: '---'
"""

import yaml

CONFIG_FILE = '.lang-config.yaml'

# loads default config by reading __doc__
default_config = lambda: yaml.load(__doc__.split('--- config ---')[1])


def merge(a, b, path=None):
    """merges dict b into dict a recursively"""
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass
            else:
                # if both a and b define the same key with
                # different values, make the values a list
                a[key] = [a[key], b[key]]
        else:
            a[key] = b[key]
    return a


def pyl(config_file=CONFIG_FILE):
    """runs PylParser using a config file returns parsed data"""
    print('running parser...')
    config = default_config()
    parser = PylParser(config)

    try:
        tmp = parser.read_all(config_file)
        config.update(yaml.load(tmp))
    except FileNotFoundError:
        pass

    tree = {'__config__': config}

    for f in config['include']:
        parser.parse(f.split('/')[-1], parser.read_all_lines(f))
        tree = merge(tree, parser.tree)

    print('parsing complete\n')
    return tree


class PylParser:

    def __init__(self, config: dict):
        self.config = config

    def parse(self, file_name: str, lines: list):
        """parses lines using syntax defined in the config"""
        self.tree = {}
        syntax = self.config
        open_tag = '__head__'
        open_rule = None
        open_rule_buffer = ''
        new_line_buffer = ''
        buffer_count = 0

        if 'EOF:' not in lines:
            lines.append('EOF:')

        def store_and_clear_buffers():
            """store open definition and clear all content buffers"""
            nonlocal new_line_buffer, open_rule_buffer, buffer_count

            try:
                self.store_rule(open_tag, open_rule, open_rule_buffer)
            except KeyError:
                self.error('__head__ does not define "lang"', file_name, 0, '')

            open_rule_buffer = ''
            new_line_buffer = ''
            buffer_count += 1

        for i in range(len(lines)):
            raw_ln = lines[i].replace('\t', syntax['INDENT'])
            ln = raw_ln.strip()

            # empty line
            if ln == '':
                new_line_buffer += syntax['NEW_LINE']
                continue

            # comment
            if raw_ln[0] == syntax['COMMENT']:
                continue

            # separates the head from the body
            # (optional if tags are defined in the body)
            if ln == syntax['SEP']:
                store_and_clear_buffers()
                if open_tag == '__head__':
                    open_tag = self.config['fallback-tag']
                else:
                    open_tag = '__head__'
                continue

            # defines a new tag
            if ln[0] == syntax['OPEN_TAG']:
                store_and_clear_buffers()
                if ln[-1] == syntax['CLOSE_TAG']:
                    open_tag = ln[1:-1]
                else:
                    open_tag = ln[1:]
                continue

            # unindented block
            if raw_ln[0] != syntax['INDENT']:
                if ln.count(syntax['OPEN_DEF']) == 1 \
                   and ln[-1] == syntax['OPEN_DEF']:
                    # multiline definition
                    store_and_clear_buffers()
                    open_rule = ln[:-1]
                    continue

                # inline definition
                tmp = ln.split(syntax['OPEN_DEF'])

                if len(tmp) >= 2:
                    store_and_clear_buffers()
                    open_rule = tmp[0]
                    open_rule_buffer = ':'.join(tmp[1:])
                    store_and_clear_buffers()
                    continue

                if ln == syntax['END_DEF']:
                    store_and_clear_buffers()
                    continue

            # there is currently an open rule
            # append its contents
            if open_rule is not None and raw_ln[0] == syntax['INDENT']:
                if open_rule_buffer != '':
                    # add spacing
                    open_rule_buffer += syntax['INDENT']
                open_rule_buffer += new_line_buffer + ln
                new_line_buffer = ''
                continue

            # we still don't know what to do with this line
            # this must be a syntax error
            self.error('Unexpected line', file_name, i, raw_ln)

        print('parsed %d definitions from %s' % (buffer_count, file_name))
        return self.tree

    def error(self, message: str, file_name: str, line_num: int, ln: str):
        """prints error message and location of error then exits the program"""
        print('ERROR: %s (%s at line %d)' % (message, file_name, line_num + 1))
        print('    >%s...' % ln[:48])
        print(self.tree)
        exit(-1)

    def store_rule(self, tag: str, rule: str, contents: str):
        """stores a new definition in the tree"""
        if contents == '':
            return

        rule = rule.strip()
        contents = contents.strip()

        if tag == '__head__':
            if tag not in self.tree:
                self.tree[tag] = {}
            self.tree[tag][rule] = contents
            return

        z = tag

        if self.config['output-structure'] == 'one-lang-per-file':
            tag = self.tree['__head__']['lang']
            tmp = rule
            rule = z
            z = tmp
        elif self.config['output-structure'] == 'one-tag-per-file':
            z = self.tree['__head__']['lang']

        if tag not in self.tree:
            self.tree[tag] = {}

        if rule not in self.tree[tag]:
            self.tree[tag][rule] = {}
        else:
            print('Warning: "%s" defined multiple times in [%s]' % (rule, tag))

        if 'lang' not in self.tree['__head__']:
            raise KeyError()

        self.tree[tag][rule][z] = contents

    def read_all_lines(self, file_name: str):
        with open(file_name, 'r') as f:
            return f.readlines()

    def read_all(self, file_name: str):
        with open(file_name, 'r') as f:
            return f.read()
