# This repo has been moved to gitlab
# https://gitlab.com/grgvt/sdltm2tmx

# sdltm2tmx

This is a command line utility and library for converting sdltm translation memories into tmx 1.4 memories.

I can't guarantee it works with every sdltm translation memory.
Please submit a bug report if you have issues.


## Usage:
cli:
To use the command line application run `sdltm2tmx [SDLTM_PATH] (optional)[SAVE_DIR]`.
Paths are either absolute or relative to the current directory. The default save directory is the current working directory.

sdltm2tmx can also be used as a library. The `run` function is the main entry point. The `TmxConverter` class does most of the real work.

Invalid segments are logged and skipped.


License GPL v.3
Copyright (c) 2018, 2019, 2022 Gregory Vigo Torres
