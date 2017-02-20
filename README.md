#sdltm2tmx#

This is a rather simple script to convert an sdltm translation memory into a tmx1.4 translation memory, in particular for use with OmegaT.

I can't guarantee this will work with every sdltm. This is really a beta/initial release, because I haven't totally reverse engineered the sdltm yet. In particular, I'm pretty sure it will fail when there is more than one tm referenced in the sdltm. That will probably be fixed as needed in a later version.


##Installation##
**sdltm2tmx** is pure Python 3 and has no dependencies.
It's been tested with Python 3.6, but it should work with any Python 3 version.


##Usage:##
cli:
The cli script must be executable e.g. `chmod 755 cli.py` then execute cli.py.
Paths are either absolute or relative to current directory.

For use as a library in other programs, call the run function of sdltm2tmx with the path to the sdltm file and the root path where you want to save the tmx.


##ToDo:##
* gui interface
* make it run a little faster


License GPL v.3
Copyright 2017, Gregory Vigo Torres
