import re
import constants
from app_exceptions import AppException
from kodi_items import *


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
        # map for regular expression (path) to method (names)
        self._dict_path = {}

        """
        Test each method of this class for the appended attribute '_re_match' by the
        decorator (RegisterProviderPath).
        The '_re_match' attributes describes the path which must match for the decorated method.
        """
        for method_name in dir(self):
            method = getattr(self, method_name)
            if hasattr(method, 're_path'):
                self.register_path(method.re_path, method_name)
                pass
            pass

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
                pass
            pass
        raise AppException("Mapping for path '%s' not found" % path)

    @RegisterPath('^/$')
    def on_root(self, context, re_match):
        result = list()
        genres_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.GENRES_LABEL),
                                    context.create_uri(), '')
        result.append(genres_item)
        popular_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.POPULAR_LABEL),
                                     context.create_uri(), '')
        result.append(popular_item)
        search_item = DirectoryItem('[B]%s[/B]' % context.localize(constants.SEARCH_LABEL),
                                    context.create_uri(), '')
        result.append(search_item)
        return result

    def tear_down(self, context):
        pass
