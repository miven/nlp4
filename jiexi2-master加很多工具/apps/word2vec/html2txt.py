#!/usr/bin/env python
#-*- coding: utf-8 -*-

import HTMLParser
import urllib
import os.path, os
import sys


class parseText(HTMLParser.HTMLParser):
    def handle_data(self, data):
        if data != '\n' and data.isspace():
            pass
        else:
            self.text.append(data)

def main(htmlpath, outpath):
    lParser = parseText()
    namelist = os.listdir(htmlpath)
    if os.path.exists(outpath):
        sys.exit()
    else:
        os.mkdir(outpath)

    for name in namelist:
        lParser.text = []
        lParser.feed('dasfdsfadsf')
        lParser.close()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
