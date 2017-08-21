import xbmcgui
import xbmcplugin
from app_exceptions import AppException
from kodi_items import *
import kodi_info_labels

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

        if isinstance(result, bool) and not result:
            xbmcplugin.endOfDirectory(context.get_handle(), succeeded=False)
        elif isinstance(result, VideoItem):
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
            xbmcplugin.endOfDirectory(context.get_handle(), succeeded=True)
        else:
            pass

    def _set_resolved_url(self, context, base_item, succeeded=True):
        item = self._to_video_item(context, base_item)
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

    def _to_video_item(self, context, video_item):
        context.log_debug('Converting VideoItem')
        major_version = context.get_system_version().get_version()[0]
        thumb = video_item.get_image() if video_item.get_image() else u'DefaultVideo.png'
        title = video_item.get_title() if video_item.get_title() else video_item.get_name()
        fanart = ''
        settings = context.get_settings()
        item = xbmcgui.ListItem(label=title)
        if video_item.get_fanart() and settings.show_fanart():
            fanart = video_item.get_fanart()
        if major_version <= 12:
            item.setIconImage(thumb)
            item.setProperty("Fanart_Image", fanart)
        elif major_version <= 15:
            item.setArt({'thumb': thumb, 'fanart': fanart})
            item.setIconImage(thumb)
        else:
            item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': fanart})

        if video_item.get_context_menu() is not None:
            item.addContextMenuItems(video_item.get_context_menu(),
                                     replaceItems=video_item.replace_context_menu())

        item.setProperty(u'IsPlayable', u'true')

        if video_item._subtitles:
            item.setSubtitles(video_item._subtitles)

        labels = kodi_info_labels.from_item(context, video_item)

        if 'duration' in labels:
            duration = labels['duration']
            del labels['duration']
            item.addStreamInfo('video', {'duration': duration})

        item.setInfo(type=u'video', infoLabels=labels)
        return item

    def _add_video(self, context, video_item, item_count=0):
        item = self._to_video_item(context, video_item)
        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=video_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
