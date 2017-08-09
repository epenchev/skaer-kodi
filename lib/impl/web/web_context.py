class WebContext(object):
    def __init__(self, path=u'/', params=None, plugin_name=u'', plugin_id=u''):
        pass

    def log_warning(self, text):
        # self.log(text, constants.log.WARNING)
        pass

    def log_error(self, text):
        # self.log(text, constants.log.ERROR)
        pass

    def log_notice(self, text):
        # self.log(text, constants.log.NOTICE)
        pass

    def log_debug(self, text):
        # self.log(text, constants.log.DEBUG)
        pass

    def log_info(self, text):
        # self.log(text, constants.log.INFO)
        pass

    def get_system_version(self):
        pass

    def get_name(self):
        return 'Skaer'

    def get_version(self):
        return '0.0.1'

    def get_path(self):
        pass

    def get_params(self):
        pass
