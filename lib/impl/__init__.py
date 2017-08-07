__author__ = 'tickbg'

__all__ = ['Runner', 'Context']

try:
    from kodi.kodi_runner import KodiRunner as Runner
    from kodi.kodi_context import KodiContext as Context
    from kodi.kodi_app import KodiApp as AppControl
except ImportError:
    from web.web_runner import WebRunner as Runner
    from web.web_context import WebContext as Context
    from web.web_app import WebApp as AppControl
    pass
