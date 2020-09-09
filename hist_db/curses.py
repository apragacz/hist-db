from __future__ import absolute_import, print_function, unicode_literals
import contextlib
import curses
import logging
import re

from .utils import pad_with_spaces

logger = logging.getLogger(__name__)


class Color(object):
    DEFAULT = 0
    SELECTED = 1


def paint_window(stdscr, model):
    height, width = stdscr.getmaxyx()
    prompt_height = 1
    prompt_width = max(0, width - 1)
    lines_capacity = max(0, height - prompt_height - 1)
    model.lines_capacity = lines_capacity
    y = lines_capacity
    for i, line in enumerate(model.matching_lines):
        color_num = Color.SELECTED if i == model.position else Color.DEFAULT
        y = lines_capacity - 1 - i
        if y < 0:
            break

        assert i < lines_capacity
        line = re.sub(r'[^\x00-\x7F]+', '?', line)
        line_padded = pad_with_spaces(' ' + line, width)
        stdscr.addnstr(y, 0, line_padded, width, curses.color_pair(color_num))

    # Clear the remaining lines without stdscr.clear()
    empty_line_padded = ' ' * width
    while y >= 0:
        stdscr.addnstr(y, 0, empty_line_padded, width, curses.color_pair(Color.DEFAULT))
        y -= 1

    # Clear the prompt line
    stdscr.addnstr(height - 1, 0, ' ' * prompt_width, prompt_width)

    prompt = '$ '
    prompt_and_search = prompt + model.search_string
    stdscr.addnstr(height - 1, 0, prompt_and_search, prompt_width)
    stdscr.refresh()


@contextlib.contextmanager
def ui_ctx():
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(Color.SELECTED, 0, 7)
        stdscr.keypad(True)
        yield stdscr
    finally:
        if stdscr:
            stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
