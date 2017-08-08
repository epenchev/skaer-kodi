__author__ = 'tickbg'


class KodiSettings(object):
    def __init__(self, xbmc_addon):
        self._xbmc_addon = xbmc_addon

    def get_string(self, setting_id):
        return self._xbmc_addon.getSetting(setting_id)

    def set_string(self, setting_id, value):
        self._xbmc_addon.setSetting(setting_id, value)

    def get_int(self, setting_id, default_value):
        value = self.get_string(setting_id)
        if value is None or value == '':
            return default_value
        try:
            return int(value)
        except ValueError:
            return default_value

    def set_int(self, setting_id, value):
        if isinstance(value, int):
            self.set_string(setting_id, str(value))
        pass

    def set_bool(self, setting_id, value):
        if not isinstance(value, bool):
            return
        if value:
            self.set_string(setting_id, 'true')
        else:
            self.set_string(setting_id, 'false')

    def get_bool(self, setting_id, default_value):
        value = self.get_string(setting_id)
        if value is None or value == '':
            return default_value

        if value != 'false' and value != 'true':
            return default_value
        return value == 'true'
