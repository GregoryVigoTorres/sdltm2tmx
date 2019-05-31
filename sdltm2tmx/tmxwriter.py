"""
Copyright (C) 2018/2019 Gregory Vigo Torres

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
import xml.dom

from lxml import etree

from sdltm2tmx import config


log = logging.getLogger(__name__)


def mk_doctype():
    dom = xml.dom.getDOMImplementation()
    tmxdoctype = dom.createDocumentType("tmx",
                                        None,
                                        config.TMX_DTD_NAME)
    return tmxdoctype.toxml()


# def mk_header(header_attrs):
#     hdr_el = etree.Element('header', **header_attrs)
#     return hdr_el


def writer(dest, header_attrs={}):
    """
    Incremental XML writer
    """
    doctype = mk_doctype()
    with etree.xmlfile(dest, encoding='utf-8') as tmx:
        tmx.write_declaration(doctype=doctype)
        with tmx.element('tmx', attrib={'version': config.TMX_VERSION}):
            hdr = etree.Element('header', **header_attrs)
            tmx.write(hdr, pretty_print=True)
            with tmx.element('body'):
                try:
                    while 1:
                        el = yield
                        tmx.write(el, pretty_print=True)
                        tmx.flush()
                        el = None
                except GeneratorExit:
                    pass

