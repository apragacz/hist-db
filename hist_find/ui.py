from __future__ import print_function, unicode_literals
import contextlib
import curses

from .utils import pad_with_spaces

COLOR_NUM_DEFAULT = 0
COLOR_NUM_HIGHLIGHT = 1


def paint_window(stdscr, model):
    height = curses.LINES
    width = curses.COLS
    prompt_height = 1
    lines_capacity = height - prompt_height
    model.lines_capacity = lines_capacity
    stdscr.clear()
    for i, line in enumerate(model.matching_lines):
        color_num = (COLOR_NUM_HIGHLIGHT if i == model.position
                     else COLOR_NUM_DEFAULT)
        y = lines_capacity - 1 - i
        if y < 0:
            break

        assert i < lines_capacity
        line_padded = pad_with_spaces(line, width)
        stdscr.addnstr(y, 0, line_padded, width, curses.color_pair(color_num))
    prompt = '$ '
    prompt_and_search = prompt + model.search_string
    stdscr.addnstr(height - 1, 0, prompt_and_search, width)
    stdscr.refresh()


@contextlib.contextmanager
def curses_ctx():
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 0, 7)
        stdscr.keypad(True)
        yield stdscr
    finally:
        if stdscr:
            stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
