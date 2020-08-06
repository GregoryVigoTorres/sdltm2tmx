# sdltm2tmx

This is a command line utility and library for converting sdltm translation memories into tmx 1.4 memories.

I can't guarantee it works with every sdltm translation memory.
Please submit a bug report if you have issues.


## Installation
Requires Python 3
Tested with Python 3.6, 3.7 and 3.8, but most likely compatible with Python 3.3 or later.
Install with `python3 setup.py` or `cd` into directory with `setup.py` and run `pip install .`


## Usage:
cli:
To use the command line application run `sdltm2tmx [SDLTM_PATH] (optional)[SAVE_DIR]`.
Paths are either absolute or relative to the current directory. The default save directory is the current working directory.

sdltm2tmx can also be used as a library. The `run` function is the main entry point. The `TmxConverter` class does most of the real work.

Invalid segments are logged and skipped.


## Changelog:
### v2.0.0 - 31/05/2019
#### Removed
- tmx_writer is no longer a dependency. An internal incremental xml writer is used instead.


License GPL v.3
Copyright (c) 2018, 2019 Gregory Vigo Torres
