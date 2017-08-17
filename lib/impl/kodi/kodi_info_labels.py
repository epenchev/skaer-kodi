from kodi_items import *


def _process_date(info_labels, param):
    if param is not None and param:
        pass

def _process_int_value(info_labels, name, param):
    if param is not None:
        info_labels[name] = int(param)

def _process_string_value(info_labels, name, param):
    if param is not None:
        info_labels[name] = unicode(param)


def _process_video_dateadded(info_labels, param):
    if param is not None and param:
        info_labels['dateadded'] = param

def _process_video_duration(context, info_labels, param):
    if param is not None:
        info_labels['duration'] = '%d' % param

def _process_video_rating(info_labels, param):
    if param is not None:
        rating = float(param)
        if rating > 10.0:
            rating = 10.0
        if rating < 0.0:
            rating = 0.0
        info_labels['rating'] = rating

def _process_list_value(info_labels, name, param):
    if param is not None and isinstance(param, list):
        info_labels[name] = param

def _process_mediatype(info_labels, name, param):
    info_labels[name] = param

def from_item(context, item):
    info_labels = {}

    # 'date' = '09.03.1982'
    _process_date(info_labels, item.get_date())

    # Video
    if isinstance(item, VideoItem):
        # mediatype
        _process_mediatype(info_labels, 'mediatype', item.get_mediatype())

        # play count
        _process_int_value(info_labels, 'playcount', item.get_play_count())

        # 'artist' = [] (list)
        _process_list_value(info_labels, 'artist', item.get_artist())

        # 'dateadded' = '2014-08-11 13:08:56' (string) will be taken from 'date'
        _process_video_dateadded(info_labels, item.get_date())

        # TODO: starting with Helix this could be seconds
        # 'duration' = '3:18' (string)
        _process_video_duration(context, info_labels, item.get_duration())

        # 'rating' = 4.5 (float)
        _process_video_rating(info_labels, item.get_rating())

        # 'director' = 'Steven Spielberg' (string)
        _process_string_value(info_labels, 'director', item.get_director())

        # 'episode' = 12 (int)
        _process_int_value(info_labels, 'episode', item.get_episode())

        # 'season' = 12 (int)
        _process_int_value(info_labels, 'season', item.get_season())

        # 'plot' = '...' (string)
        _process_string_value(info_labels, 'plot', item.get_plot())

        # 'code' = 'tt3458353' (string) - imdb id
        _process_string_value(info_labels, 'code', item.get_imdb_id())

        # 'cast' = [] (list)
        _process_list_value(info_labels, 'cast', item.get_cast())

    return info_labels
