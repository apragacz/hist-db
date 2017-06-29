from __future__ import print_function, unicode_literals
import curses
import logging
import os
from curses.ascii import ctrl

logger = logging.getLogger(__name__)

FILE_LOG_FORMAT = ("%(levelname).3s %(asctime)s %(name)s: "
                   "%(message)s [%(filename)s:%(lineno)d]")


KEY_REVERSE_SEARCH = ctrl(ord('r'))
KEY_EXIT = ctrl(ord('g'))
KEY_ESCAPE = 27
COLOR_NUM_DEFAULT = 0
COLOR_NUM_HIGHLIGHT = 1

EXIT_KEY_SEQUENCES = {
    KEY_EXIT,
    KEY_ESCAPE,
}


pressed_codes = []
search_chars = []
position = -1


def move_position_up():
    global position
    position += 1


def move_position_down():
    global position
    if position < 0:
        return
    position -= 1


def clear_position():
    global position
    position = -1


def pad_with_spaces(text, width):
    return text
    trimmed_text = text[:width]
    trimmed_text_len = len(trimmed_text)
    padded_text = trimmed_text + (' ' * max(0, width - trimmed_text_len))
    # padded_text = trimmed_text + (' ' * 0)
    assert len(padded_text) == width
    return padded_text


def paint_window(stdscr, matching_lines, search_string):
    height = curses.LINES
    width = curses.COLS
    prompt_height = 1
    stdscr.clear()
    for i, line in enumerate(matching_lines):
        color_num = COLOR_NUM_HIGHLIGHT if i == position else COLOR_NUM_DEFAULT
        y = height - 1 - prompt_height - i
        if y < 0:
            break
        line_padded = pad_with_spaces(line, width)
        stdscr.addnstr(y, 0, line_padded, width, curses.color_pair(color_num))
    prompt = '$ '
    prompt_and_search = prompt + search_string
    stdscr.addnstr(height - 1, 0, prompt_and_search, width)
    stdscr.refresh()


def handle_key_code(code):
    pressed_codes.append(code)
    if code in EXIT_KEY_SEQUENCES:
        raise KeyboardInterrupt()

    if code == curses.KEY_BACKSPACE:
        if search_chars:
            search_chars.pop()
    elif code in {curses.KEY_UP, KEY_REVERSE_SEARCH}:
        move_position_up()
    elif code == curses.KEY_DOWN:
        move_position_down()
    elif 32 <= code < 256:
        search_chars.append(chr(code))
        clear_position()


def main_loop(stdscr, lines):
    while True:
        search_string = ''.join(search_chars)
        matching_lines = iter_matching_lines(lines, search_string)
        paint_window(stdscr, matching_lines, search_string)
        code = stdscr.getch()
        handle_key_code(code)


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
    logging.basicConfig(
        filename='hist-find.log',
        filemode='w',
        format=FILE_LOG_FORMAT,
        level=logging.DEBUG,
    )
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 0, 7)
        stdscr.keypad(True)
        lines = list(iter_unique(iter_history_lines(is_reversed=True)))
        main_loop(stdscr, lines)
    except KeyboardInterrupt:
        pass
    finally:
        if stdscr:
            stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    logger.debug('pressed_codes %s', pressed_codes)
