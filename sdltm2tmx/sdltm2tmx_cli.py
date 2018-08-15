#! /usr/bin/env python3

import logging
import os

import click

import sdltm2tmx.config
from sdltm2tmx.sdltm2tmx import run

log = logging.getLogger(__name__)


@click.command()
@click.argument('sdltm_path',
                type=click.Path(exists=True))
@click.argument('destdir',
                required=False,
                type=click.Path(exists=False,
                                dir_okay=True,
                                file_okay=False,
                                writable=True,
                                resolve_path=True))
def main(sdltm_path, destdir=None):
    """"
    Runs the memory extractor


    Arguments
    ---------

    sdltm_path: str
        required

    destdir:
        optional, defaults to current directory

    """
    if destdir is None:
        destdir = os.path.abspath(os.curdir)

    run(sdltm_path, destdir)


if __name__ == '__main__':
    main()
