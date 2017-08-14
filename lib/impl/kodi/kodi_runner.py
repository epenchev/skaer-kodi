import xbmcgui
import xbmcplugin
from app_exceptions import AppException
from kodi_items import *


class KodiRunner(object):
    def __init__(self):
        pass

    def run(self, app_control=None, context=None):
        results = None
        try:
            results = app_control.navigate(context)
        except AppException as ex:
            context.log_error(ex.get_message())
            xbmcgui.Dialog().ok("Exception in Application Control", ex.get_message())
            return

        result = results[0]
        options = {}
        options.update(results[1])

        '''
        Original code, activate after test

        if isinstance(result, bool) and not result:
            xbmcplugin.endOfDirectory(context.get_handle(), succeeded=False)
        elif isinstance(result, VideoItem) or isinstance(result, AudioItem) or isinstance(result, UriItem):
            self._set_resolved_url(context, result)
        elif isinstance(result, DirectoryItem):
            self._add_directory(context, result)
        elif isinstance(result, list):
            item_count = len(result)
            for item in result:
                if isinstance(item, DirectoryItem):
                    self._add_directory(context, item, item_count)
                elif isinstance(item, VideoItem):
                    self._add_video(context, item, item_count)
                elif isinstance(item, AudioItem):
                    self._add_audio(context, item, item_count)
                elif isinstance(item, ImageItem):
                    self._add_image(context, item, item_count)
                pass

            xbmcplugin.endOfDirectory(
                context.get_handle(), succeeded=True,
                cacheToDisc=options.get(Abstractapp_control.RESULT_CACHE_TO_DISC, True))
        else:
            # TODO handle exception
            pass
        '''
        if isinstance(result, bool) and not result:
            xbmcplugin.endOfDirectory(context.get_handle(), succeeded=False)
        elif isinstance(result, DirectoryItem):
            self._add_directory(context, result)
        elif isinstance(result, list):
            item_count = len(result)
            for item in result:
                if isinstance(item, DirectoryItem):
                    self._add_directory(context, item, item_count)
        xbmcplugin.endOfDirectory(context.get_handle(), succeeded=True)

    def _set_resolved_url(self, context, base_item, succeeded=True):
        item = xbmc_items.to_item(context, base_item)
        item.setPath(base_item.get_uri())
        xbmcplugin.setResolvedUrl(context.get_handle(), succeeded=succeeded, listitem=item)

    def _add_directory(self, context, directory_item, item_count=0):
        item = xbmcgui.ListItem(label=directory_item.get_name(),
                                iconImage=u'DefaultFolder.png',
                                thumbnailImage=directory_item.get_image())
        settings = context.get_settings()
        if directory_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', directory_item.get_fanart())
        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=directory_item.get_uri(),
                                    listitem=item,
                                    isFolder=True,
                                    totalItems=item_count)

    def _add_video(self, context, video_item, item_count=0):
        item = xbmc_items.to_video_item(context, video_item)
        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=video_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)