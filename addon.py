__author__ = 'tickbg'

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import sys

addon = xbmcaddon.Addon(id='plugin.video.skaer')
plugin_handle = int(sys.argv[1]) if len(sys.argv) > 1 else None

def create_items():
    listing = []
    listing.append( 'The first item' )
    listing.append( 'The second item' )
    listing.append( 'The third item' )
    listing.append( 'The fourth item' )
    return listing

def kodigui_run(gui_items):
    global plugin_handle
    for item in gui_items:
        list_item = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(plugin_handle, '', list_item)
        # tell kodi we have finished creating the directory listing
        xbmcplugin.endOfDirectory(plugin_handle)

kodigui_run(create_items())