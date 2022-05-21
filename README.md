# firefox sync tabs to bookmarks file

Export tabs from Firefox Sync into bookmarks file

Latest version available from https://github.com/clach04/firefox_sync_tabs_to_bookmarks_file

Export tabs from Firefox sync using https://github.com/eNote-GmbH/syncclient (https://github.com/clach04/firefox_syncclient - enote_docs branch)

Works with Python 3.x or 2.7.


## Setup

Issue:

    #pip install git+https://github.com/eNote-GmbH/syncclient.git  # does NOT work after install as of 2022-05-21 due to path issues
    git clone https://github.com/eNote-GmbH/syncclient
    cd firefox_syncclient
    pip install -e .
    python syncclient/main.py --help

## Usage

Sample:

    # firefox_syncclient
    fxa-client -v -u me@example.com --account-server https://api.accounts.firefox.com/v1 --oauth-server https://oauth.accounts.firefox.com/v1 --bearer
    python syncclient/main.py -u me@example.com --client-id $CLIENT_ID --decrypt get_records tabs > export.json  # from https://github.com/eNote-GmbH/syncclient

    # firefox_sync_tabs_to_bookmarks_file
    python3 dump_tabs_bookmark.py export.json  # list client names
    python3 dump_tabs_bookmark.py export.json "client name"  # dump bookmarks for device called "client name"
    python3 dump_tabs_bookmark.py export.json -a  # dump bookmarks of tabs for all devices - NOTE export format untested with other tools

Bookmark file is in NETSCAPE Bookmark file format. Suitable for import into most tools.
For example:

  * Shiori
  * Wallabag
  * Firefox

Running notes:

  * if tab history is present script will stop, first entry in history can be used and the rest dropped if environment variable `IGNORE_HISTORY` is set
  * Recommend using Python3 and under Microsoft Windows setting `set PYTHONIOENCODING=utf8` to ensure stdout redirect to file works correctly


NOTE firefox_syncclient is likely not an ideal tool/version.

Check out:

  * https://github.com/nafonels/syncclient/compare/master...tcr:master  -- not sure why json load is done in put_record()
  * https://github.com/mozilla-services/syncclient/issues/28 - avoid "New sign-in to Firefox" email confirmation/warning
  * https://github.com/eNote-GmbH/syncclient - NOTE not been able to successfully use this to export data, unclear on usage (missing docs)
    error `fxa.errors.ClientError: The request was blocked for security reasons`
    https://github.com/eNote-GmbH/syncclient/pull/2
