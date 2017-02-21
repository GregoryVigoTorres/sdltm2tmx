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

import xml.dom
import xml.dom.minidom


class TmxWriter():
    def __init__(self, tmx_properties, segments, tmxpath=None):
        """
        version 1.0
        segments is a generator
        """
        self.source_language = tmx_properties['source_language'].upper()
        self.target_language = tmx_properties['target_language'].upper()
        self.segments = segments

        self.header_properties = {'srclang': self.source_language,
                                  'creationtool': 'sdltm2tmx',
                                  'creationtoolversion': '0.1',
                                  'segtype': 'sentence',
                                  'o-tmf': 'sdltm',
                                  'adminlang': 'en-us',
                                  'datatype': 'plaintext'}

        self.tmx = self.create_document()
        self.add_headers()
        body = self.tmx.getElementsByTagName('body')
        self.body = body[0]
        tus = self.gen_tu()
        [self.body.appendChild(tu) for tu in tus]

    def make_tuv(self, seg, src=False):
        """
        make source or target tuv element
        target tuvs have some additional attributes
        """
        tuv = self.tmx.createElement('tuv')

        if src:
            tuv.setAttribute('lang', self.source_language)
            seg = self.make_seg(seg['source_segment'])
            tuv.appendChild(seg)
        else:
            tuv.setAttribute('lang', self.target_language)
            tuv.setAttribute('changeid', seg.get('creation_user'))
            tuv.setAttribute('creationdate', seg.get('creation_date'))
            tuv.setAttribute('changedate', seg.get('change_date'))
            tuv.setAttribute('changeuser', seg.get('change_user'))
            seg = self.make_seg(seg['target_segment'])
            tuv.appendChild(seg)

        return tuv

    def make_seg(self, text):
        seg = self.tmx.createElement('seg')
        tn = self.tmx.createTextNode(text.strip())
        seg.appendChild(tn)
        return seg

    def gen_tu(self):
        """
        generator for tu elements with tuv and seg elements
        """
        for seg in self.segments:
            tu = self.tmx.createElement('tu')
            src_tuv = self.make_tuv(seg, src=True)
            tar_tuv = self.make_tuv(seg, src=False)
            tu.appendChild(src_tuv)
            tu.appendChild(tar_tuv)
            yield tu

    def create_document(self):
        """
        uses xml.dom to create document with correct doctype
        """
        dom = xml.dom.getDOMImplementation()
        tmxdoctype = dom.createDocumentType("tmx",
                                            None,
                                            "tmx14.dtd")
        tmx = dom.createDocument("http://www.lisa.org/tmx14",
                                 "tmx",
                                 tmxdoctype)

        return tmx

    def add_headers(self):
        root = self.tmx.documentElement
        attr = self.tmx.createAttribute('version')
        root.setAttributeNode(attr)
        root.setAttribute('version', '1.4')

        headerelem = self.tmx.createElement('header')
        for k in self.header_properties.keys():
            attr = self.tmx.createAttribute(k)
            headerelem.setAttributeNode(attr)
            headerelem.setAttribute(k, self.header_properties[k])

        root.appendChild(headerelem)

        note = self.tmx.createElement('note')
        note_text = self.tmx.createTextNode('Created from sdltm')
        note.appendChild(note_text)
        headerelem.appendChild(note)

        bodyelem = self.tmx.createElement('body')
        self.tmx.documentElement.appendChild(bodyelem)

    def save(self, tmxpath):
        try:
            with open(tmxpath, mode='w') as tm:
                self.tmx.writexml(tm,
                                  indent='',
                                  addindent=' ',
                                  newl='\n',
                                  encoding='UTF-8')
                tm.close()
            return (True, None)
        except Exception as E:
            return (False, E)
