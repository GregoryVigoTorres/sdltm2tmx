"""
Copyright (C) 2017 Gregory Vigo Torres

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

from datetime import datetime
import re
import os
import sqlite3
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

from .tmxlib import TmxWriter


sdl_date_fmt = '%Y-%m-%d %H:%M:%S'
iso_8601 = '%Y%m%dT%H%M%SZ'
src = ''
tmx_save_root = ''


def get_invalid_characters(seg):
    chars = ''
    for i in seg:
        if i == '<':
            return chars
        chars += i


def parse_tu(seg):
    """
    parse translation segment XML

    Segments that cannot be parsed are skipped
    and an error is logged.
    """
    try:
        line = ET.fromstring(seg)
        for i in line.iter():
            if i.tag.lower() == 'value':
                return re.sub('\s+', ' ', i.text)
    except ParseError as E:
        print(E.msg)
        bad_chars = get_invalid_characters(seg[E.position[1]:])
        print('Invalid characters: {0}\n'.format(bad_chars))
        return


def fmt_date(date_str):
    """
    tmx dates should be in ISO 8601 format
    YYYYMMDDThhmmssZ

    original format is like:
    2017-02-07 07:38:21

    strptime -> date obj
    strftime -> str
    """
    od = datetime.strptime(date_str, sdl_date_fmt)
    iso_date = datetime.strftime(od, iso_8601)
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


def run(src, tmx_save_root):
    tmx_save_root = tmx_save_root

    print('opening tm: {}'.format(src))
    conn = sqlite3.connect(src)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    tm_props = get_translation_memory_props(c)
    props = {k: tm_props[k] for k in tm_props.keys()}
    tm_id = props.get('id')
    segments = get_segments(c, tmid=tm_id)

    print('generating tmx...')
    writer = TmxWriter(props, segments)
    tm_name = props.get('name')

    if not tm_name:
        tm_name = 'sdltm2tmx'
    else:
        tm_name = re.sub('\s', '_', tm_name)
        tm_name = tm_name.replace('/', '')

    save_path = os.path.join(tmx_save_root, tm_name)
    save_path += '.tmx'
    success, reason = writer.save(save_path)

    if not success:
        print('Error saving {}'.format(save_path))
        print(reason)
        conn.rollback()
    else:
        print('tmx saved to {}'.format(save_path))

    conn.close()
