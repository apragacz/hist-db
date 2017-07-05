from __future__ import print_function, unicode_literals
import fcntl
import termios


def fill_terminal(line):
    for c in line:
        fcntl.ioctl(0, termios.TIOCSTI, c)


def escape_single_quote(text):
    segments = text.split('\'')
    return '"\'"'.join('\'' + s + '\'' for s in segments)
