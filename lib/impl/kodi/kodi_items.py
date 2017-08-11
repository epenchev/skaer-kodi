import hashlib


class BaseItem(object):
    def __init__(self, name, uri, image=u'', fanart=u''):
        self._name = unicode(name)
        self._uri = str(uri)
        self._image = u''
        self.set_image(image)
        self._fanart = fanart

    def get_id(self):
        """
        Returns a unique id of the item.
        """
        m = hashlib.md5()
        m.update(self._name.encode('utf-8'))
        m.update(self._uri.encode('utf-8'))
        return m.hexdigest()

    def get_name(self):
        return self._name

    def set_uri(self, uri):
        if isinstance(uri, str):
            self._uri = uri
        else:
            self._uri = ''

    def get_uri(self):
        return self._uri

    def set_image(self, image):
        if image is None:
            self._image = u''
        else:
            self._image = image

    def get_image(self):
        return self._image

    def set_fanart(self, fanart):
        self._fanart = fanart

    def get_fanart(self):
        return self._fanart


class DirectoryItem(BaseItem):
    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        self._plot = unicode(name)

    def set_name(self, name):
        self._name = unicode(name)

    def set_plot(self, plot):
        self._plot = unicode(plot)

    def get_plot(self):
        return self._plot
