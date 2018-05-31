# py.lang

This is a document format for use in localizing text. Each document defines strings of a language, this can then be compiled to csv, json or xml.

## Running

```bash
pyhton3 pylcsv.py
python3 pyljson.py
python3 pylxml.py
```

## Get Started

Document structure:

```yaml
lang: English
author: User
contact: user@company.com

---

greeting:
  Hello World!
```

Check out the [basic document example](./examples/basic.lang) and the [multi document example](./examples/multi-doc.lang) for more.

## Configuration

`pyl` is configured using a `.lang-config.yaml` file.

Basic configuration:

```yaml
# list of input file paths
include:
  - ./path/to/first/file.lang
  - ./path/to/second/file.lang

# output directory path
output: ./output
```

For the complete configuration file (including syntax definitions) check out the [example config](./examples/.lang-config.yaml)

## Custom compiler

`pyl.py` parses .lang files using a `.lang-config.yaml` file as input and returns the parsed tree.

```python
import pyl

tree = pyl.pyl(config_file='.lang-config.yaml')
print(tree)
```
