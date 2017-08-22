#!/usr/bin/env python

from lib import scraper

def main():
    s = scraper.MediaScraper()
    genres = s.avail_genres()
    movies = s.movies_info(genres['Action'])
    plist = s.media_url(movies.iteritems().next()[1].get('movid'))
    print(plist)
    # TODO a caokie test
    for cookie in iter(s._cookiejar):
        print '%s :' % cookie.name  + ' %s' % cookie.value
    # res = s.search("Rambo")
    # print(res)

if __name__ == '__main__':
    main()
