import sys
import urllib
import urlparse
import weakref
import datetime
import json

import xbmc
import xbmcaddon
import xbmcplugin

import constants
from kodi_settings import KodiSettings
from kodi_version import KodiVersion


class KodiContext(object):
    def __init__(self):
        self._addon = xbmcaddon.Addon()
        self._system_version = None
        self._params = dict()

        # path of the uri
        self._uri = sys.argv[0]
        comps = urlparse.urlparse(self._uri)
        self._path = urllib.unquote(comps.path).decode('utf-8')

        # get the params
        if len(sys.argv) > 2:
            params = sys.argv[2][1:]
            if len(params) > 0:
                self._uri = self._uri + '?' + params
                params = dict(urlparse.parse_qsl(params))
                for par in params:
                    item = params[par]
                    self._params[par] = item.decode('utf-8')
                pass
            pass
        pass

        self._plugin_handle = int(sys.argv[1]) if len(sys.argv) > 1 else None
        self._plugin_id = self._addon.getAddonInfo('id')
        self._plugin_name = self._addon.getAddonInfo('name')
        self._version = self._addon.getAddonInfo('version')
        self._native_path = xbmc.translatePath(self._addon.getAddonInfo('path'))
        self._settings = KodiSettings(self._addon)

    def _log(self, text, log_level=constants.LOG_NOTICE):
        log_line = '[%s] %s' % (self.get_id(), text)
        xbmc.log(msg=log_line, level=log_level)

    def get_settings(self):
        return self._settings

    def get_path(self):
        return self._path

    def get_params(self):
        return self._params

    def get_param(self, name, default=None):
        return self.get_params().get(name, default)

    def get_handle(self):
        return self._plugin_handle

    def get_native_path(self):
        return self._native_path

    def get_id(self):
        return self._plugin_id

    def get_name(self):
        return self._plugin_name

    def get_system_version(self):
        if not self._system_version:
            self._system_version = KodiVersion()
        return self._system_version

    def get_version(self):
        return self._version

    def localize(self, text_id, default_text=u''):
        if isinstance(text_id, int):
            if text_id:
                result = xbmc.getLocalizedString(text_id)

                self.log_notice(result)

                if result is not None and result:
                    return result.decode('utf-8')
        return default_text.decode('utf-8')

    def _create_path(self, *args):
        comps = []
        for arg in args:
            if isinstance(arg, list):
                return self._create_path(*arg)

            comps.append(unicode(arg.strip('/').replace('\\', '/').replace('//', '/')))

        uri_path = '/'.join(comps)
        if uri_path:
            return u'/%s/' % uri_path

        return '/'

    def _create_uri_path(self, *args):
        comps = []
        for arg in args:
            if isinstance(arg, list):
                return self._create_uri_path(*arg)
            comps.append(arg.strip('/').replace('\\', '/').replace('//', '/').encode('utf-8'))

        uri_path = '/'.join(comps)
        if uri_path:
            return urllib.quote('/%s/' % uri_path)

        return '/'

    def create_uri(self, path=u'/', params=None):
        if not params:
            params = {}
        uri = self._create_uri_path(path)
        if uri:
            uri = "%s://%s%s" % ('plugin', self._plugin_id.encode('utf-8'), uri)
        else:
            uri = "%s://%s/" % ('plugin', self._plugin_id.encode('utf-8'))

        if len(params) > 0:
            # make a copy of the map
            uri_params = {}
            uri_params.update(params)

            # encode in utf-8
            for param in uri_params:
                if isinstance(params[param], int):
                    params[param] = str(params[param])
                uri_params[param] = to_utf8(params[param])
            uri += '?' + urllib.urlencode(uri_params)
            pass
        return uri

    def log_warning(self, text):
        self._log(text, constants.LOG_WARNING)

    def log_error(self, text):
        self._log(text, constants.LOG_ERROR)

    def log_notice(self, text):
        self._log(text, constants.LOG_NOTICE)

    def log_debug(self, text):
        self._log(text, constants.LOG_DEBUG)

    def log_info(self, text):
        self._log(text, constants.LOG_INFO)
