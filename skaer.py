#!/usr/bin/env python

from lib import scraper

def main():
    s = scraper.MediaScraper()
    genres = s.avail_genres()
    movies = s.movies_info(genres['Action'])
    plist = s.media_url(movies.iteritems().next())
    print(plist)
    # res = s.search("Rambo")
    # print(res)

if __name__ == '__main__':
    main()
