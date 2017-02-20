#! /usr/bin/env python3

from sdltm2tmx import run


if __name__ == '__main__':
    src = input('Path to sdltm > ')
    tmx_save_root = input('Directory to save tmx in > ')
    run(src, tmx_save_root)
