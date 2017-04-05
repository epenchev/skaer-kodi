#!/usr/bin/env python

import os
import re
import sys
import urllib, urllib2
import cookielib

BASE_URL = 'https://yesmovies.to'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

def get_headers_list():
    return { 'User-Agent' : USER_AGENT }

class SpiderEngine(object):
    def __init__(self):
        self.genres = {}
        self.movies = {}
        self.tagparser = None

    def get_genres(self):
        try:
            req = urllib2.Request(BASE_URL, None, get_headers_list())
            response = urllib2.urlopen(req)
            response_data = response.read()
            response.close()
            rgx = '<a href=\"(\S+/genre/\S+)\" title=\"(\S+)\"'
            for r in re.finditer(rgx , response_data):
                self.genres[r.group(2)] = r.group(1)
        except urllib2.URLError, e:
            if e.code == 403 or e.code == 401:
                print('Got error response code')
        return self.genres

    def get_movie_list(self, url):
        try:
            req = urllib2.Request(url, None, get_headers_list())
            response = urllib2.urlopen(req)
            response_data = response.read()
            response.close()
            rgx = '<a href=\S+ class=\"ml-mask\" title=\"(.+)\"\s+data-url=\"(\S+)\">\s.+\s.+<.+\s+data-original=\"(\S+)\"'
            for r in re.finditer(rgx , response_data):
                self.movies[r.group(1)] = {'api_url' : BASE_URL + '/' + r.group(2), 'img' : r.group(3)}
        except urllib2.URLError, e:
            if e.code == 403 or e.code == 401:
                print('Got error response code')


def main():
    spider = SpiderEngine()
    genres = spider.get_genres()
    spider.get_movie_list(genres['Kungfu'])
    print(spider.movies)

if __name__ == '__main__':
    main()
