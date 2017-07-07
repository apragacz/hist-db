from __future__ import absolute_import, print_function, unicode_literals
import os


def iter_history_lines(is_reversed=False):
    if is_reversed:
        for line in reversed(list(iter_history_lines(is_reversed=False))):
            yield line
        return
    with open(get_history_path(), 'r') as f:
        for line in f:
            yield line.rstrip()


def get_history_path():
    return os.path.join(os.environ['HOME'], '.bash_history')
