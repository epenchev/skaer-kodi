import re
import constants
from app_exceptions import AppException
from kodi_items import *
from lib.scraper import *


class RegisterPath(object):
    def __init__(self, re_path):
        self._re_path = re_path

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.re_path = self._re_path
        return wrapper


class KodiApp(object):
    def __init__(self):
        self._scrapper = MediaScraper()

        # map for regular expression (path) to method (names)
        self._dict_path = {}
        for method_name in dir(self):
            method = getattr(self, method_name)
            if hasattr(method, 're_path'):
                self.register_path(method.re_path, method_name)

    def register_path(self, re_path, method_name):
        self._dict_path[re_path] = method_name

    def navigate(self, context):
        path = context.get_path()
        for key in self._dict_path:
            re_match = re.search(key, path, re.UNICODE)
            if re_match is not None:
                method_name = self._dict_path.get(key, '')
                method = getattr(self, method_name)
                if method is not None:
                    result = method(context, re_match)
                    if not isinstance(result, tuple):
                        result = result, {}
                    return result
        raise AppException("Mapping for path '%s' not found" % path)

    @RegisterPath('^/$')
    def _on_root(self, context, re_match):
        result = list()
        genres_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.GENRES_LABEL),
                                    context.create_uri(['genres']), '')
        result.append(genres_item)
        popular_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.POPULAR_LABEL),
                                     context.create_uri(['popular']), '')
        result.append(popular_item)
        search_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.SEARCH_LABEL),
                                    context.create_uri(['search']), '')
        result.append(search_item)
        return result

    @RegisterPath('^/genres/(?P<genre>.*)/$')
    def _on_genres(self, context, re_match):
        result = list()
        genres = self._scrapper.avail_genres()
        selected_genre = re_match.group('genre')
        # Just for the test !!!
        if selected_genre is not None:
            result.append(DirectoryItem('[B]%s[/B]' % selected_genre,
                          context.create_uri(['genres', selected_genre]), ''))
            return result

        for name in genres.iterkeys():
            result.append(DirectoryItem('[B]%s[/B]' % name,
                          context.create_uri([name]), ''))
        return result

    def tear_down(self, context):
        pass
