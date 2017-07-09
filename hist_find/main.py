from __future__ import absolute_import, print_function, unicode_literals
import argparse
import logging
import os.path
import sys
from curses import KEY_BACKSPACE, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
from curses.ascii import ctrl

from .config import load_config
from .history import iter_history_lines
from .model import Model
from .curses import ui_ctx, paint_window
from .term import escape_single_quote, fill_terminal

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
    done = False
    logger.debug("processing code %s", ch)

    if ch in EXIT_KEY_SEQUENCES:
        raise KeyboardInterrupt()

    if ch == KEY_BACKSPACE:
        model.remove_character()
    elif ch in {KEY_UP, KEY_REVERSE_SEARCH}:
        model.move_position_up()
    elif ch == KEY_DOWN:
        model.move_position_down()
    elif ch == KEY_ENTER:
        model.action = Model.Action.EXECUTE
        done = True
    elif ch == KEY_LEFT:
        model.action = Model.Action.EDIT
        done = True
    elif ch == KEY_RIGHT:
        model.action = Model.Action.FILL
        done = True
    elif 32 <= ch < 256:
        model.append_character(chr(ch))
    return done


def handle_action(model):
    best_matching_line = model.best_matching_line
    action = model.action
    logger.info('best_matching_line %s', best_matching_line)
    if best_matching_line is None:
        return
    if action == Model.Action.EXECUTE:
        fill_terminal(best_matching_line + '\n')
    elif action == Model.Action.FILL:
        fill_terminal(best_matching_line)
        print('\n', file=sys.stderr)
    elif action == Model.Action.EDIT:
        escaped_line = escape_single_quote(best_matching_line)
        fill_terminal('fc ' + escaped_line + '\n')


def main_interactive_loop(model):
    with ui_ctx() as stdscr:
        done = False
        while not done:
            paint_window(stdscr, model)
            ch = stdscr.getch()
            done = handle_key_press(ch, model)


def setup_logging(config):
    logging_config = config['logging']
    filepath = os.path.expanduser(logging_config['file'])
    filemode = 'a' if logging_config['append'] else 'w'
    level_str = logging_config['level']
    level_for_str = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'fatal': logging.FATAL,
    }
    level = level_for_str.get(level_str, logging.INFO)
    logging.basicConfig(
        filename=filepath,
        filemode=filemode,
        format=FILE_LOG_FORMAT,
        level=level,
    )
    logger.info('config: %s', config)


def get_parser():
    parser = argparse.ArgumentParser(prog='hist-find')
    parser.add_argument('search_terms', nargs='*')
    return parser


def main():
    try:
        config = load_config()
        setup_logging(config)
        parser = argparse.ArgumentParser(prog='hist-find')
        parser.add_argument('search_terms', nargs='*')
        args = parser.parse_args()
        search_string = ' '.join(args.search_terms)
        model = Model(
            iter_history_lines(is_reversed=True),
            search_string=search_string,
        )
        main_interactive_loop(model)
        handle_action(model)
    except KeyboardInterrupt:
        pass
