[![PyPI version](https://badge.fury.io/py/pngminifier.svg)](https://badge.fury.io/py/pngminifier)

Program for chunk-level PNG manipulation. Strips out ancillary information (eg. EXIF tags).

```
usage: __main__.py [-h] [-o OUTPUT] [--include-useful] [INPUT]

positional arguments:
  INPUT             input PNG file to read from, by default stdin

optional arguments:
  -h, --help        show this help message and exit
  -o OUTPUT         output PNG file to write to, by default stdout
  --include-useful  include useful chunks too (not recommended)
```

By default it lets through bare-minimum of chunks required for proper functionality (IHDR, IDAT, IEND, PLTE)
and chunks that it deems *useful* (gAMA, tRNS, iCCP) if `--include-useful` is specified. All other chunks are
discarded to maintain standard compliance.
