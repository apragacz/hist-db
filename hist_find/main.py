from __future__ import print_function, unicode_literals
import curses
from curses.ascii import ctrl

EXIT_KEY_SEQUENCES = {
    ctrl(ord('g')),  # Ctrl + G
    27,  # ESC
}
keys = []


def main_loop(stdscr):
    while True:
        c = stdscr.getch()
        keys.append(c)
        if c in EXIT_KEY_SEQUENCES:
            break


def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    try:
        main_loop(stdscr)
    except KeyboardInterrupt:
        pass
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    print(keys)
