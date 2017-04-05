#!/usr/bin/env python

import os
import re
import sys
import urllib, urllib2
import cookielib
import unicodedata
from HTMLParser import HTMLParser

BASE_URL = 'https://yesmovies.to'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

def get_headers_list():
    return { 'User-Agent' : USER_AGENT }


class HTMLTagParser(HTMLParser):
    def __init__(self, caller):
        HTMLParser.__init__(self)
        self._tag = None
        self._attrs = {}
        self._caller = caller

    def handle_starttag(self, tag, attrs):
        self._tag = tag
        self._attrs.clear()
        self._attrs = {name: value for name, value in attrs}
        self._caller(tag, self._attrs)


class SpiderEngine(object):
    def __init__(self):
        self.genres = {}

    def get_genres(self):
        if len(self.genres):
            return self.genres
        try:
            req = urllib2.Request(BASE_URL, None, get_headers_list())
            response = urllib2.urlopen(req)
            tagparser = HTMLTagParser(self.extract_genre)
            response_data = response.read()
            response.close()
            tagparser.feed(response_data)
            return self.genres
        except urllib2.URLError, e:
            if e.code == 403 or e.code == 401:
                print('Got error response code')
        return self.genres

    def extract_genre(self, tag, attrs):
        if tag == 'a' and 'title' in attrs and 'href' in attrs:
            mch = re.match(BASE_URL + '/genre\S+' , attrs['href'])
            if mch:
                self.genres[attrs['href']] = attrs['title']


def main():
    spider = SpiderEngine()
    print(spider.get_genres())

if __name__ == '__main__':
    main()
