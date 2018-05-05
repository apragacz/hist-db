from __future__ import absolute_import, print_function, unicode_literals
import os
from collections import OrderedDict

import six
from six.moves.configparser import ConfigParser, NoSectionError


CONFIG_DEFAULTS = {
    'logging': {
        'file': '~/.hist-db.log',
        'append': True,
        'level': 'error',
    },
}


def get_default_config_path():
    return os.path.join(os.environ['HOME'],
                        '.config', 'hist-db', 'config.ini')


def load_config(config_path=None, defaults=None):
    if config_path is None:
        config_path = get_default_config_path()
    if defaults is None:
        defaults = CONFIG_DEFAULTS
    config_parser = ConfigParser()
    config_parser.read([config_path])
    config = OrderedDict()

    for section_name, default_section_data in six.iteritems(defaults):
        config_section = config.setdefault(section_name, OrderedDict())
        for param_name, default_value in six.iteritems(default_section_data):
            config_section[param_name] = _get_config_value(
                config_parser, section_name, param_name, default_value)

    return config


def _get_config_value(config_parser, section_name, param_name, default_value):
    try:
        if isinstance(default_value, bool):
            return config_parser.getboolean(section_name, param_name)
        elif isinstance(default_value, float):
            return config_parser.getfloat(section_name, param_name)
        elif isinstance(default_value, int):
            return config_parser.getint(section_name, param_name)
        else:
            return config_parser.get(section_name, param_name)
    except (ValueError, NoSectionError):
        return default_value
