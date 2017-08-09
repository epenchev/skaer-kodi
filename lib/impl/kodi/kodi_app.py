import re
from app_exceptions import AppException


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
            if hasattr(method, 'kodion_re_path'):
                self.register_path(method.kodion_re_path, method_name)
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

    def on_root(self, context, re_match):
        pass

    def tear_down(self, context):
        pass
