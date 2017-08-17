import hashlib


class BaseItem(object):
    def __init__(self, name, uri, image=u'', fanart=u''):
        self._name = unicode(name)
        self._uri = str(uri)
        self._image = u''
        self.set_image(image)
        self._fanart = fanart

    def get_id(self):
        """
        Returns a unique id of the item.
        """
        m = hashlib.md5()
        m.update(self._name.encode('utf-8'))
        m.update(self._uri.encode('utf-8'))
        return m.hexdigest()

    def get_name(self):
        return self._name

    def set_uri(self, uri):
        if isinstance(uri, str):
            self._uri = uri
        else:
            self._uri = ''

    def get_uri(self):
        return self._uri

    def set_image(self, image):
        if image is None:
            self._image = u''
        else:
            self._image = image

    def get_image(self):
        return self._image

    def set_fanart(self, fanart):
        self._fanart = fanart

    def get_fanart(self):
        return self._fanart


class DirectoryItem(BaseItem):
    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        self._plot = unicode(name)

    def set_name(self, name):
        self._name = unicode(name)

    def set_plot(self, plot):
        self._plot = unicode(plot)

    def get_plot(self):
        return self._plot


class VideoItem(BaseItem):
    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        self._genre = None
        self._duration = None
        self._director = None
        self._episode = None
        self._season = None
        self._year = None
        self._plot = None
        self._title = name
        self._imdb_id = None
        self._cast = None
        self._rating = None
        self._artist = None
        self._play_count = None
        self._mediatype = None
        self._subtitles = None

    def set_play_count(self, play_count):
        self._play_count = int(play_count)

    def get_play_count(self):
        return self._play_count

    def add_artist(self, artist):
        if self._artist is None:
            self._artist = []
        self._artist.append(unicode(artist))

    def get_artist(self):
        return self._artist

    def set_title(self, title):
        self._title = unicode(title)
        self._name = self._title

    def get_title(self):
        return self._title

    def set_plot(self, plot):
        self._plot = unicode(plot)

    def get_plot(self):
        return self._plot

    def set_rating(self, rating):
        self._rating = float(rating)

    def get_rating(self):
        return self._rating

    def set_director(self, director_name):
        self._director = unicode(director_name)

    def get_director(self):
        return self._director

    def add_cast(self, cast):
        if self._cast is None:
            self._cast = []
        self._cast.append(cast)

    def get_cast(self):
        return self._cast

    def set_imdb_id(self, url_or_id):
        re_match = __RE_IMDB__.match(url_or_id)
        if re_match:
            self._imdb_id = re_match.group('imdbid')
        else:
            self._imdb_id = url_or_id

    def get_imdb_id(self):
        return self._imdb_id

    def set_episode(self, episode):
        self._episode = int(episode)

    def get_episode(self):
        return self._episode

    def set_season(self, season):
        self._season = int(season)

    def get_season(self):
        return self._season

    def set_duration(self, hours, minutes, seconds=0):
        _seconds = seconds
        _seconds += minutes * 60
        _seconds += hours * 60 * 60
        self.set_duration_from_seconds(_seconds)

    def set_duration_from_minutes(self, minutes):
        self.set_duration_from_seconds(int(minutes) * 60)

    def set_duration_from_seconds(self, seconds):
        self._duration = int(seconds)

    def get_duration(self):
        return self._duration

    def set_genre(self, genre):
        self._genre = unicode(genre)

    def get_genre(self):
        return self._genre

    def set_date(self, year, month, day, hour=0, minute=0, second=0):
        date = datetime.datetime(year, month, day, hour, minute, second)
        self._date = date.isoformat(sep=' ')

    def set_date_from_datetime(self, date_time):
        self.set_date(year=date_time.year, month=date_time.month, day=date_time.day, hour=date_time.hour,
                      minute=date_time.minute, second=date_time.second)

    def get_date(self):
        return self._date

    def set_mediatype(self, mediatype):
        self._mediatype = mediatype

    def get_mediatype(self):
        if self._mediatype not in ['video', 'movie', 'tvshow', 'season', 'episode', 'musicvideo']:
            self._mediatype = 'video'
        return self._mediatype

    def set_subtitles(self, value):
        self._subtitles = value if value and isinstance(value, list) else None
