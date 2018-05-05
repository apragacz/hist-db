from __future__ import absolute_import, print_function, unicode_literals
import argparse
import logging
import os.path

from .config import load_config
from .search import find

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


def find_action(config, args):
    start_search_string = ' '.join(args.search_terms)
    find(config, start_search_string)


def main(args=None):
    config = load_config()
    setup_logging(config)

    parser = argparse.ArgumentParser(prog='hist-db')
    subparsers = parser.add_subparsers(help='sub-command help')

    find_parser = subparsers.add_parser('find')
    find_parser.add_argument('search_terms', nargs='*')
    find_parser.set_defaults(action=find_action)

    parser_args = parser.parse_args(args=args)
    parser_action = parser_args.action
    parser_action(config, parser_args)
