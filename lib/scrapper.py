import re
import time
import urllib, urllib2

class MediaScraper:
    BASE_URL = 'https://yesmovies.to/'

    def _headers(self):
        return {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        }

    def get_genres(self):
        genres = {}
        try:
            req = urllib2.Request(MediaScraper.BASE_URL, None, self._headers())
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            for r in re.finditer('<a href=\"(\S+/genre/\S+)\" title=\"(\S+)\"' , data):
                genre_name, genre_url = r.group(2), r.group(1)
                genres[genre_name] = genre_url
        except urllib2.URLError, e:
            if e.code != 200:
                print ('skaer: {0}'.format(e.reason))
        return genres

    def get_movies(self, url):
        movies = {}
        try:
            req = urllib2.Request(url, None, self._headers())
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
        except urllib2.URLError, e:
            if e.code != 200:
                print ('skaer: {0}'.format(e.reason))
        else:
            for r in re.finditer('<a href=\S+ class=\"ml-mask\" title=\"(.+)\"\s+data-url=\"(\S+)\">'
                                 '\s.+\s.+<.+\s+data-original=\"(\S+)\"', data):
                info_url = MediaScraper.BASE_URL + r.group(2)
                found = re.search('(\d+)\.html', info_url)
                if found:
                    movies[r.group(1)] = {
                        'movid' : found.group(1),
                        'info_url' : info_url,
                        'img_url' : r.group(3),
                    }
        return movies

    def _urlopen(self, url):
        print(url)
        try:
            req = urllib2.Request(url, None, self._headers())
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            if e.code != 200:
                print ('skaer: {0}'.format(e.reason))
        except socket.error as e:
            print ('skaer: {0}'.format(e.reason))
        return None

    def _source_ids(self, data):
        ids = []
        for r in re.finditer('data-server=\\\\"\d+\\\\".data-id=\\\\"(\d+)', data):
            ids.append(r.group(1))
        return ids

    def _movie_token(self, eid):
        pass

    def media_url(self, movie):
        movid = movie[1]['movid']
        data = self._urlopen(MediaScraper.BASE_URL + 'ajax/v4_movie_episodes' + '/' + movid)
        # Fetch auth tokens
        if data is not None:
            ids = self._source_ids(data)
            # TODO check ids
            print(ids)
            for eid in ids:
                data = self._urlopen(
                    MediaScraper.BASE_URL + 'ajax/movie_token?eid=' + eid + 
                    '&mid=' + movid + '&_=' + str(int(time.time())))
                if data is not None:
                    print(data)
                    result = re.match('_x=\'(\S+)\', _y=\'(\S+)\'', data)
                    if result is not None:
                        data = self._urlopen(
                            MediaScraper.BASE_URL + 'ajax/movie_sources/' + eid +
                            '?x=' + result.group(1) + '&y=' + result.group(2))
                        print(data)
        return None
