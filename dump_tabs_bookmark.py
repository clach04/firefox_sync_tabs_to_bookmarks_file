#!/usr/bin/env python3
# -*- coding: ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
# pretty json demo
"""take firefox synx tab info json file export and dump into NETSCAPE-Bookmark-file html file
suitable for import into most tools.

does not attempt to handle unicode, expects py3 (rather than py2) to handle that, even under Windows.

Works fine interactive but redirecting to file needs:

    set PYTHONIOENCODING=utf8
    export PYTHONIOENCODING=utf8

to avoid:

      File ".....\Python\Python37\lib\encodings\cp1252.py", line 19, in encode
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]
    UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f98a' in position 134: character maps to <undefined>

Usage:

    python3 dump_tabs_bookmark.py export.json  # list clients
    python3 dump_tabs_bookmark.py export.json "client name"  # dump bookmarks

Where export.json can be generated using https://github.com/clach04/firefox_syncclient :

    python syncclient/main.py alexis@notmyidea.org $PASSWORD get_records tabs > export.json
"""

try:
    from html import escape
except ImportError:
    from cgi import escape
import os
import sys
import warnings
import logging

# json support, TODO consider http://pypi.python.org/pypi/omnijson
try:
    #raise ImportError()
    # Python 2.6+
    import json
except ImportError:
    try:
        #raise ImportError()
        # from http://code.google.com/p/simplejson
        import simplejson as json
    except ImportError:
        json = None

logging.basicConfig() ## NO debug, no info. But logs warnings
log = logging.getLogger("mylogger")
log.setLevel(logging.DEBUG)


def naive_dump_json(x, indent=None):
    """dumb not safe!
    Works for the purposes of this specific script as quotes never
    appear in data set.
    
    Parameter indent ignored"""
    warnings.warn('about to dump rough read_json')
    assert isinstance(x, dict)
    # could use pprint for the purposes of this specific script
    return repr(x).replace("'", '"')

def naive_load_json(x):
    """dumb not safe! Works for the purposes of this specific script
    
    Has one advantage over real json/simpljson libs, it handles firefox
    bookmarks.json exports
    """
    warnings.warn('about to evaluate/execute potentially unsafe code (read_json)')
    null = None
    return eval(x)


if json is None:
    dump_json = naive_dump_json
    load_json = naive_load_json
else:
    dump_json = json.dumps
    load_json = json.loads
"""TODO json document api and validators consider:
  * http://pypi.python.org/pypi/json-document/0.1.devdf66fa9
  * http://pypi.python.org/pypi/json_rest/ - not suitable but approach is nice
  * http://pypi.python.org/pypi/validictory
  * http://pypi.python.org/pypi/micromodels
  * http://pypi.python.org/pypi?%3Aaction=search&term=json+rest&submit=search
  * http://deron.meranda.us/python/demjson/ lists other json encoders/decoders (min 2.3 for demjson)
      * http://deron.meranda.us/python/comparing_json_modules/
"""


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    filename = argv[1]
    try:
        client_name = argv[2]
    except IndexError:
        client_name = None
    ignore_history = os.environ.get('IGNORE_HISTORY', False)
    #ignore_history = True
    if client_name == '-a':
        dump_all = True
    else:
        dump_all = False

    log.info('filename %r', filename)
    f = open(filename, 'rb')
    data = f.read()
    log.info('read complete, len %r', len(data))
    f.close()
    
    # Firefox bookmark JSON output always ends in:  '.....:[]},]}'
    # note the comma 3 from the end. According to
    #    http://code.google.com/p/simplejson/issues/detail?id=44
    # this is not valid JSON (although it is valid ECMA/Javascript)
    #
    # ValueError: Expecting object: line 1 column 1480482 (char 1480482)
    #print 'extract %r' % data[1480482-10:1480482+20]
    log.info('extract %r', data[-10:])
    #data data de-encoding..... from UTF8
    tmp_data = load_json(data)
    log.debug('load complete')

    """
    pretty_json = dump_json(tmp_data, indent=4, sort_keys=True)  # , ensure_ascii=False  ?
    print(pretty_json)
    log.debug('dump complete')
    """
    netscape_bookmark_file_template = """<!DOCTYPE NETSCAPE-Bookmark-file-1><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks</H1>
<DL>
    <DT><H3>Optional Folder Name</H3><DL>
        <DT><A HREF="https://github.com/go-shiori/shiori/wiki/Usage" >go-shiori/shiori</A>
    </DL><!-- optional, only if H3 folder name was used -->
</DL>
"""  # FIXME actual use a template
    if client_name:
        print('''<!DOCTYPE NETSCAPE-Bookmark-file-1><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"><TITLE>Bookmarks</TITLE><H1>Bookmarks</H1><DL>''')

    for device in tmp_data:
        if client_name:
            if dump_all:
                print('<DT><H3>%s</H3><DL>' % device["payload"]["clientName"])
            if dump_all or client_name == device["payload"]["clientName"]:
                for tab in device["payload"]["tabs"]:
                    #print(repr(tab["title"]))
                    #print(len(tab["urlHistory"]))
                    if len(tab["urlHistory"]) != 1 and not ignore_history:
                        print('************')
                        print(repr(tab["title"]))
                        print(len(tab["urlHistory"]))
                        print(tab["urlHistory"])
                        raise NotImplementedError('lengths != 1 (%r)' % len(tab["urlHistory"]))
                    url = tab["urlHistory"][0]
                    title = tab["title"]
                    print('''<DT><A HREF="%s" >%s</A>''' % (url, escape(title)))
            if dump_all:
                print('</DL>')
        else:
            print(device["payload"]["clientName"])

    if client_name:
        print('''</DL>''')
            
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


