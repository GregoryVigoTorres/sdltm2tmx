# sdltm2tmx

This is a command line utility and library for converting sdltm translation memories into tmx 1.4 memories.

I can't guarantee it works with every sdltm translation memory.
Please submit a bug report if you have issues.


## Installation
Requires Python3
Tested with Python 3.6 and 3.7, but most likely compatible with Python 3.3 or later.
Depends on tmx-writer, which can be found at [https://gitlab.com/grgvt/tmx_writer.git](https://gitlab.com/grgvt/tmx_writer.git).
Install with `python3 setup.py`


## Usage:
cli:
To use the command line application run `sdltm2tmx $SDLTM_PATH (optional)$SAVE_DIR`.
Paths are either absolute or relative to the current directory. The default save directory is the current working directory.

sdltm2tmx can also be used as a library. The `run` function is the main entry point.

Segments with invalid XML are logged and skipped.


License GPL v.3
Copyright (c) 2017, 2018 Gregory Vigo Torres
