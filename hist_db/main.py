from __future__ import absolute_import, print_function, unicode_literals
import argparse
import logging
import os.path

from .config import load_config

logger = logging.getLogger(__name__)

FILE_LOG_FORMAT = "%(levelname).3s %(asctime)s %(name)s: %(message)s [%(filename)s:%(lineno)d]"  # noqa: E501


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


def search_action(config, args):
    from hist_db.search import start_search
    start_search_string = ' '.join(args.search_terms)
    start_search(config, start_search_string)


def append_action(config, args):
    pass


def shell_config_show_action(config, args):
    from hist_db.shell_config import show_shell_config
    show_shell_config(config)


def main(args=None):
    config = load_config()
    setup_logging(config)

    parser = argparse.ArgumentParser(prog='hist-db')
    subparsers = parser.add_subparsers(help='sub-command help')

    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('--reverse', action='store_true')
    search_parser.add_argument('--forward', action='store_true')
    search_parser.add_argument('search_terms', nargs='*')
    search_parser.set_defaults(action=search_action)

    append_parser = subparsers.add_parser('append')
    append_parser.set_defaults(action=append_action)

    shell_config_parser = subparsers.add_parser('shell-config')
    shell_config_subparsers = shell_config_parser.add_subparsers()

    shell_config_show_parser = shell_config_subparsers.add_parser('show')
    shell_config_show_parser.set_defaults(action=shell_config_show_action)

    parser_args = parser.parse_args(args=args)
    parser_action = parser_args.action
    parser_action(config, parser_args)
