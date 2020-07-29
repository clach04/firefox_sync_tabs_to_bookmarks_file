# firefox_sync_tabs_to_bookmarks_file

Export tabs from Firefox Sync into bookmarks file

Latest version available from https://github.com/clach04/firefox_sync_tabs_to_bookmarks_file

Export tabs from Firefox sync using https://github.com/clach04/firefox_syncclient

Sample:

    # firefox_syncclient
    python syncclient/main.py alexis@notmyidea.org $PASSWORD get_records tabs > export.json

    # firefox_sync_tabs_to_bookmarks_file
    python3 dump_tabs_bookmark.py export.json  # list clients
    python3 dump_tabs_bookmark.py export.json "client name"  # dump bookmarks

Bookmark file is in NETSCAPE Bookmark file format. Suitable for import into most tools.
For example:

  * Shiori
  * Wallabag
  * Firefox
