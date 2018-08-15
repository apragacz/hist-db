from __future__ import absolute_import, print_function, unicode_literals
import os
import sys

if sys.version_info[0] >= 3:
    open_unicode = open
else:
    import codecs
    open_unicode = codecs.open


def iter_history_lines(is_reversed=False):
    if is_reversed:
        for line in reversed(list(iter_history_lines(is_reversed=False))):
            yield line
        return
    with open_unicode(get_history_path(), mode='rt', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip()


def get_history_path():
    return os.path.join(os.environ['HOME'], '.bash_history')
