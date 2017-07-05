from __future__ import print_function, unicode_literals
import curses
import logging
from curses.ascii import ctrl

from .history import iter_history_lines
from .model import Model
from .ui import curses_ctx, paint_window
from .term import fill_terminal

logger = logging.getLogger(__name__)

FILE_LOG_FORMAT = ("%(levelname).3s %(asctime)s %(name)s: "
                   "%(message)s [%(filename)s:%(lineno)d]")


KEY_REVERSE_SEARCH = ctrl(ord('r'))
KEY_EXIT = ctrl(ord('g'))
KEY_ESCAPE = 27
KEY_ENTER = 10

EXIT_KEY_SEQUENCES = {
    KEY_EXIT,
    KEY_ESCAPE,
}


def handle_key_press(ch, model):
    logger.debug("processing code %s", ch)

    if ch in EXIT_KEY_SEQUENCES:
        raise KeyboardInterrupt()

    if ch == curses.KEY_BACKSPACE:
        model.remove_character()
    elif ch in {curses.KEY_UP, KEY_REVERSE_SEARCH}:
        model.move_position_up()
    elif ch == curses.KEY_DOWN:
        model.move_position_down()
    elif ch == KEY_ENTER:
        model.set_accepted()
        return False
    elif 32 <= ch < 256:
        model.append_character(chr(ch))
    return True


def main_loop(model):
    with curses_ctx() as stdscr:
        while True:
            paint_window(stdscr, model)
            ch = stdscr.getch()
            if not handle_key_press(ch, model):
                break


def main():
    logging.basicConfig(
        filename='hist-find.log',
        filemode='w',
        format=FILE_LOG_FORMAT,
        level=logging.DEBUG,
    )
    try:
        model = Model(iter_history_lines(is_reversed=True), 1)
        main_loop(model)
        if model.action == Model.Action.ACCEPTED:
            fill_terminal(model.best_matching_line)
    except KeyboardInterrupt:
        pass
