#!/usr/bin/env python

from lib import scrapper

def main():
    s = scrapper.MediaScraper()
    genres = s.get_genres()
    movies = s.get_movies(genres['Action'])
    s.media_url(movies.iteritems().next())

if __name__ == '__main__':
    main()
