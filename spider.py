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

class MyHTMLParser(HTMLParser):
    def __init__(self, state):
        HTMLParser.__init__(self)
        self.found_genres = False
        self._tag = None
        self._attrs = {}
        self._state = state

    def check_tag_attr(self, tagname, attrname, attrval):        
        if self._tag == tagname:
            if attrname in self._attrs:
                if self._attrs[attrname] == attrval:
                    return True
        return False

    def get_tag_attr(self, tagname, attrname):
        if self._tag == tagname and attrname in self._attrs:
            return self._attrs[attrname]
        return None

    def handle_starttag(self, tag, attrs):
        self._tag = tag
        self._attrs.clear()
        self._attrs = {name: value for name, value in attrs}
        self._state.on_starttag(tag, self)

    def handle_endtag(self, tag):
        self._state.on_endtag(tag, self)

    def handle_data(self, data):
        # print "Encountered some data  :", data
        pass


class ParserState(object):
    def __init__(self):
        self.found_genres = False
        self.found_country = False
        self.sub_menu = False
        self.
        self.genres = []
        self.genres_urls = []

    def on_starttag(self, tag, parser):
        if parser.check_tag_attr('a', 'title', 'Genre'):
            self.found_genres = True
            return
        if parser.check_tag_attr('ul', 'class', 'sub-menu') and self.found_genres:
            self.sub_menu = True
            return
        if self.found_genres and self.sub_menu:
            genre = parser.get_tag_attr('a', 'title')
            if genre:
                self.genres.append(genre)
            link = parser.get_tag_attr('a', 'href')
            if link:
                self.genres_urls.append(link)

    def on_endtag(self, tag, parser):
        if self.found_genres and tag == 'ul':
            self.found_genres = False


def get_headers_list():
    return { 'User-Agent' : USER_AGENT }

def main():
    try:
        req = urllib2.Request(BASE_URL, None, get_headers_list())
        response = urllib2.urlopen(req)
        state = ParserState()
        parser = MyHTMLParser(state)
        response_data = response.read()
        parser.feed(response_data)
        print(state.genres)
        print(state.genres_urls)
        response.close()
    except urllib2.URLError, e:
        if e.code == 403 or e.code == 401:
            print('Got error response code')


if __name__ == '__main__':
    main()
