"""
Copyright (C) 2018 Gregory Vigo Torres

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see http://www.gnu.org/licenses/.
"""
import logging
import os
import re
import sqlite3
from datetime import datetime
from xml.etree import ElementTree as ET

from sdltm2tmx.config import (
    ISO_8601_FMT,
    SDL_DATE_FMT
)
from sdltm2tmx.db import session
from tmx_writer import TmxWriter


log = logging.getLogger(__name__)


def parse_tu(seg):
    """
    Parse translation segment XML and return segment text
    Invalid segments are logged & discarded
    The error message doesn't show the right position, but it's not my fault
    """
    try:
        line = ET.fromstring(seg)
        return line.findtext('.//Value') or line.findtext('.//value')
    except ET.ParseError as E:
        log.error(seg)
        log.error(E.msg)


def fmt_date(date_str):
    """
    tmx dates should be in ISO 8601 format
    sdltm date format is like:
    2017-02-07 07:38:21
    """
    od = datetime.strptime(date_str, SDL_DATE_FMT)
    iso_date = datetime.strftime(od, ISO_8601_FMT)
    return iso_date


def get_seg(row):
    """
    tu - translation unit
    xml containing source or target text

    reformat dates to ISO 8601 per tmx standard
    """
    row = dict(row)
    src = row['source_segment']
    tar = row['target_segment']

    row['source_segment'] = parse_tu(src)
    row['target_segment'] = parse_tu(tar)

    row['creation_date'] = fmt_date(row['creation_date'])
    row['change_date'] = fmt_date(row['change_date'])

    return row


def gen_segs(qry):
    """
    each line contains two xml entities
    source, target
    """
    for row in qry:
        seg = get_seg(row)

        if seg['source_segment'] and seg['target_segment']:
            yield seg


def get_segments(c, tmid=None):
    """
    list of lists of text content
    source, target

    Get id for debugging
    """
    stmt = """SELECT
                id,
                source_segment,
                target_segment,
                creation_date,
                creation_user,
                change_date,
                change_user
              FROM
                translation_units
            """
    if tmid:
        stmt += """
        WHERE
        translation_memory_id = {}
        """.format(tmid)

    c.execute(stmt)
    qry = c.fetchall()
    segments = gen_segs(qry)
    return segments


def get_translation_memory_props(c):
    """
    c is the db cursor.

    It looks like there can be more than one
    translation memory in an sdltm
    So, this will have to be modified to handle that
    at some point.
    """
    stmt = """SELECT
                id,
                source_language,
                target_language,
                name,
                creation_user,
                creation_date
              FROM
                translation_memories
            """
    props = c.execute(stmt).fetchone()
    return props


def get_tm_path(props, tmx_save_root):
    tm_name = props.get('name')

    if not tm_name:
        tm_name = 'sdltm2tmx'
    else:
        tm_name = re.sub('\s', '_', tm_name)
        tm_name = tm_name.replace('/', '.')

    if not tm_name.endswith('.tmx'):
        tm_name += '.tmx'

    return os.path.join(tmx_save_root, tm_name)


def run(src, tmx_save_root):
    log.info('opening tm: {}'.format(src))
    with session(src) as c:
        tm_props = get_translation_memory_props(c)
        props = {k: tm_props[k] for k in tm_props.keys()}
        tm_id = props.get('id')

        segments = get_segments(c, tmid=tm_id)

    hdr_attrs = {'srclang': props.get('source_lanuguage')}
    tm_attrs = {'source_language':props.get('source_language'),
                'target_language':props.get('target_language')}

    writer = TmxWriter(tmx_attrs=tm_attrs, header_attrs=hdr_attrs)
    writer.feed(segments)

    save_path = get_tm_path(props, tmx_save_root)
    success, reason = writer.save(save_path)

    if not success:
        log.error('Error saving {}'.format(save_path))
        log.error(reason)
    else:
        log.info('tmx saved to {}'.format(save_path))
