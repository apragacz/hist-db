from __future__ import print_function, unicode_literals
import curses
import os
from curses.ascii import ctrl

EXIT_KEY_SEQUENCES = {
    ctrl(ord('g')),  # Ctrl + G
    27,  # ESC
}
pressed_codes = []
search_chars = []


def paint_window(stdscr, matching_lines, search_string):
    height = curses.LINES
    width = curses.COLS
    prompt_height = 1
    stdscr.clear()
    for i, line in enumerate(matching_lines):
        y = height - 1 - prompt_height - i
        if y < 0:
            break
        stdscr.addnstr(y, 0, line, width)
    prompt_and_search = '$ {search_string}'.format(search_string=search_string)
    stdscr.addnstr(height - 1, 0, prompt_and_search, width)
    stdscr.refresh()


def main_loop(stdscr, lines):
    while True:
        search_string = ''.join(search_chars)
        matching_lines = iter_matching_lines(lines, search_string)
        paint_window(stdscr, matching_lines, search_string)
        code = stdscr.getch()
        pressed_codes.append(code)
        if code in EXIT_KEY_SEQUENCES:
            break

        if code == curses.KEY_BACKSPACE:
            if search_chars:
                search_chars.pop()
        elif 32 <= code < 256:
            search_chars.append(chr(code))


def iter_matching_lines(iterator, search_string):
    for line in iterator:
        if search_string not in line:
            continue
        yield line


def iter_unique(iterator):
    lines_directory = set()
    for line in iterator:
        if line in lines_directory:
            continue
        lines_directory.add(line)
        yield line


def iter_history_lines(is_reversed=False):
    if is_reversed:
        for line in reversed(list(iter_history_lines(is_reversed=False))):
            yield line
        return
    with open(get_history_path(), 'r') as f:
        for line in f:
            yield line


def get_history_path():
    return os.path.join(os.environ['HOME'], '.bash_history')


def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    try:
        lines = list(iter_unique(iter_history_lines(is_reversed=True)))
        main_loop(stdscr, lines)
    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    print(pressed_codes)
