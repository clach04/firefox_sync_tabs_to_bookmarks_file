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


NOTE firefox_syncclient is likely not an ideal tool/version.

Check out:

  * https://github.com/nafonels/syncclient/compare/master...tcr:master  -- not sure why json load is done in put_record()
  * https://github.com/mozilla-services/syncclient/issues/28 - avoid "New sign-in to Firefox" email confirmation/warning
  * https://github.com/eNote-GmbH/syncclient - NOTE not been able to successfully use this to export data, unclear on usage (missing docs)
    error `fxa.errors.ClientError: The request was blocked for security reasons`
