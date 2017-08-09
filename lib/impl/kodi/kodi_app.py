import re
from app_exceptions import AppException


class KodiApp(object):
    def __init__(self):
        # map for regular expression (path) to method (names)
        self._dict_path = {}
        # register some default paths
        # TODO

    def register_path(self, re_path, method_name):
        """
        Registers a new method by name (string) for the given regular expression
        :param re_path: regular expression of the path
        :param method_name: name of the method
        :return:
        """
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

    def tear_down(self, context):
        pass
