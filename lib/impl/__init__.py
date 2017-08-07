__author__ = 'tickbg'

__all__ = ['Runner', 'Context']

try:
    from kodi.kodi_runner import KodiRunner as Runner
    from kodi.kodi_context import KodiContext as Context
except ImportError:
    from web.web_runner import WebRunner as Runner
    from web.web_context import WebContext as Context
    pass
