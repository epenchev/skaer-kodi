#!/usr/bin/env python

import os
import re
import sys
import urllib, urllib2
import cookielib
import js2py
import sys

BASE_URL = 'https://yesmovies.to'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
URL_EP_INFO = 'https://yesmovies.to/ajax/v4_movie_episodes/(\d+)'
URL_MOVIE_TOKEN = 'https://yesmovies.to/ajax/movie_token?eid=(\d+)&mid=(\d+)&_=unix_timestamp'
URL_MOVIE_SOURCES = 'https://yesmovies.to/ajax/movie_sources/(\d+)?x=(\S+)&y=(\S+)'

def headers():
    return { 'User-Agent' : USER_AGENT }

def execjs(jsbuf):
    rcrlm = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)
    try:
        jsfname = 'sample.js'
        jsfile = open(jsfname, 'w')
        jsfile.write(jsbuf)
        jsfile.close()
        eval_result, resobj = js2py.run_file(jsfname)
        os.remove(jsfname)
        sys.setrecursionlimit(rcrlm)
        return resobj
    except:
        print('Error executing javascript')
    return None


class SpiderEngine(object):
    def __init__(self):
        self.genres = {}
        self.movies = {}

    def getGenres(self):
        try:
            req = urllib2.Request(BASE_URL, None, headers())
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

    def getMovielist(self, url):
        try:
            req = urllib2.Request(url, None, headers())
            response = urllib2.urlopen(req)
            response_data = response.read()
            response.close()
            rgx = '<a href=\S+ class=\"ml-mask\" title=\"(.+)\"\s+data-url=\"(\S+)\">\s.+\s.+<.+\s+data-original=\"(\S+)\"'
            for r in re.finditer(rgx , response_data):
                self.movies[r.group(1)] = {'info_url' : BASE_URL + '/' + r.group(2), 'img' : r.group(3)}
        except urllib2.URLError, e:
            if e.code == 403 or e.code == 401:
                print('Got error response code')

    def _apiMovietoken(self, watch_url):
        try:
            retry = 5
            print(watch_url)
            match = re.match('-(\d+)\/(\d+)', watch_url)
            if match:
                print match.group(1)
            '''
            api_url = None
            while retry:
                req = urllib2.Request(api_url, None, headers())
                response = urllib2.urlopen(req)
                res = execjs(response.read())
                response.close()
                retry -= 1
                if res:
                    return res
            '''
        except urllib2.URLError as err:
            print(err)
        return None


    def getStream(self, name):
        if name in self.movies:
            info_url = self.movies[name]['info_url']
            try:
                req = urllib2.Request(info_url, None, headers())
                response = urllib2.urlopen(req)
                response_data = response.read()
                response.close()
                search = re.search('<a href=\"(.+\/watching.html)', response_data)
                if search:
                    self._apiMovietoken(search.group(1))
            except urllib2.URLError as err:
                print(err)
        return None


def main():
    spider = SpiderEngine()
    #genres = spider.getGenres()
    #spider.getMovielist(genres['Kungfu'])
    #print(spider.movies)
    #name = spider.movies.iterkeys().next()
    #spider.getStream(name)

if __name__ == '__main__':
    main()
