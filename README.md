# sdltm2tmx

This is a rather simple script to convert an sdltm translation memory into a tmx1.4 translation memory, in particular for use with OmegaT.

I can't guarantee this will work with every sdltm. This is a beta release, because I haven't totally reverse engineered the sdltm yet. Any issues will hopefully be resolved in later versions.


## Installation
**sdltm2tmx** has no dependencies.
It's been tested with Python 3.6, but it should work with any Python 3 version.
It can be installed with `python3 setup.py install`.


## Usage:
cli:
To run the command line application run `sdltm2tmx-cli`.
Paths are either absolute or relative to the current directory.

For use as a library in other programs, call the run function of sdltm2tmx with the path to the sdltm file and the root path where you want to save the tmx.


## ToDo:
* gui interface
* optimization may be necessary to handle really large TMs


License GPL v.3
Copyright 2017, Gregory Vigo Torres
