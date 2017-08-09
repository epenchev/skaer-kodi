import xbmc
import json


class KodiVersion(object):
    def __init__(self):
        self._version = (0, 0, 0, 0)
        self._releasename = 'UNKNOWN'
        self._releasename = 'UNKNOWN'
        self._appname = 'UNKNOWN'
        try:
            json_query = xbmc.executeJSONRPC(
                '{ "jsonrpc": "2.0", "method": "Application.GetProperties",\
                 "params": {"properties": ["version", "name"]}, "id": 1 }')

            json_query = unicode(json_query, 'utf-8', errors='ignore')
            json_query = json.loads(json_query)
            version_installed = []
            version_installed = json_query['result']['version']
            self._version = (version_installed.get('major', 1), version_installed.get('minor', 0))
            self._appname = json_query['result']['name']
            pass
        except:
            self._version = (1, 0)  # Frodo
            self._appname = 'Unknown Application'
            pass
        self._releasename = 'Unknown XBMC Release'
        if self._version >= (12, 0):
            self._releasename = 'Frodo'
            pass
        if self._version >= (13, 0):
            self._releasename = 'Gotham'
            pass
        if self._version >= (14, 0):
            self._releasename = 'Helix'
            pass
        if self._version >= (15, 0):
            self._releasename = 'Isengard'
            pass
        if self._version >= (16, 0):
            self._releasename = 'Jarvis'
            pass
        if self._version >= (17, 0):
            self._releasename = 'Krypton'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        obj_str = "%s (%s-%s)" % (self._releasename, self._appname, '.'.join(map(str, self._version)))
        return obj_str

    def get_release_name(self):
        return self._releasename

    def get_version(self):
        return self._version

    def get_app_name(self):
        return self._appname
