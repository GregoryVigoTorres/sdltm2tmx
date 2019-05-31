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
from io import BytesIO
import logging
import os
import re
import sqlite3
from datetime import datetime

from lxml import etree

from sdltm2tmx.config import (
    HEADER_ATTRS,
    ISO_8601_FMT,
    SDL_DATE_FMT
)
from sdltm2tmx.db import session
from sdltm2tmx.tmxwriter import writer


log = logging.getLogger(__name__)


class TmxConverter():
    def __init__(self, sdltm=None):
        self.src = sdltm
        self.get_tm_props()
        self.header_attrs = HEADER_ATTRS
        self.header_attrs['srclang'] = self.tm_attrs.get('source_language')
        self.header_attrs['o-tmf'] = os.path.basename(self.src)
        self.srclang = self.header_attrs['srclang']
        # segments is a generator
        self.segments = self.get_segments()

    def get_tm_props(self):
        with session(self.src) as c:
            tm_props = self.get_translation_memory_props(c)
            self.tm_attrs = {k: tm_props[k] for k in tm_props.keys()}

    # rename this
    def get_translation_memory_props(self, c):
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

    def get_segments(self):
        """
        c db cursor
        tmid self tm props
        queries db/sdltm
        returns gen_segs generator
        Get id for debugging
        """
        tmid = self.tm_attrs.get('id')
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

        with session(self.src) as c:
            c.execute(stmt)
            qry = c.fetchall()
            segments = self.gen_segs(qry)
            return segments

    def gen_segs(self, qry):
        """
        each line contains at least 2 xml fragments
        source, target
        """
        for row in qry:
            tu_data = self.get_tu_data(row)
            el = self.mk_tu_elem(tu_data)
            yield el

    def parse_orig_tuv(self, tuv):
        """
        sdltm xml segment to dict
        """
        _tuv = {}
        try:
            seg_elem = etree.fromstring(tuv)
            for elem in seg_elem.iter():
                if elem.tag.lower() == 'value':
                    _tuv['seg'] = ''.join(elem.itertext())
                if elem.tag.lower() == 'culturename':
                    _tuv['lang'] = elem.text
            return _tuv
        except Exception as E:
            log.error(E)

    def get_tu_data(self, orig_tu):
        """
        orig_tu is a query result consisting of xml containing source and target text
        Dates are reformatted to ISO 8601, per tmx standard
        Returns a list of dicts
        """
        row = orig_tu
        orig_tu = dict(orig_tu)
        tus = []
        keys = list(orig_tu.keys())
        for k in keys:
            if 'segment' in k:
                tuv = orig_tu.pop(k)
                tuv = self.parse_orig_tuv(tuv)
                if tuv.get('lang') != self.srclang:
                    # add other attrs to non-source segment
                    tuv['creationdate'] = self.fmt_date(orig_tu.get('creation_date'))
                    tuv['changedate'] = self.fmt_date(orig_tu.get('change_date'))
                    tuv['creationid'] = orig_tu.get('creation_user')
                    tuv['changeid'] = orig_tu.get('change_user')
                tus.append(tuv)
        return tus

    def fmt_date(self, date_str):
        """
        tmx dates should be in ISO 8601 format
        sdltm date format is like:
        2017-02-07 07:38:21
        """
        od = datetime.strptime(date_str, SDL_DATE_FMT)
        iso_date = datetime.strftime(od, ISO_8601_FMT)
        return iso_date

    def mk_tuv_elem(self, parent, tuv_data):
        """
        Also generates seg element children
        """
        seg_text = tuv_data.pop('seg')
        lang = tuv_data.pop('lang')
        tuv_attrs = {'lang': lang }
        if lang != self.srclang:
            tuv_attrs.update(tuv_data)
        tuv = etree.SubElement(parent, 'tuv', **tuv_attrs)
        seg = etree.SubElement(tuv, 'seg')
        seg.text = seg_text

    def mk_tu_elem(self, tu_data):
        """
        generates tu elements
        """
        tu = etree.Element('tu')
        for tuv_data in tu_data:
            self.mk_tuv_elem(tu, tuv_data)
        return tu



def get_tm_path(props, tmx_save_root):
    """
    This is for saving the converted tmx
    """
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
    converter = TmxConverter(sdltm=src)
    # write segments to tm with incremental writer
    # get header and tm attrs
    log.info(converter.segments)
    log.info(converter.header_attrs)
    _tmx = BytesIO()
    w = writer(_tmx)

    return
    # save_path = get_tm_path(props, tmx_save_root)
    # success, reason = writer.save(save_path)

    # if not success:
    #     log.error('Error saving {}'.format(save_path))
    #     log.error(reason)
    # else:
    #     log.info('tmx saved to {}'.format(save_path))
