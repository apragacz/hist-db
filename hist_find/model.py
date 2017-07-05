from __future__ import print_function, unicode_literals
import itertools

from .utils import iter_unique, iter_matching_lines


class Model(object):

    class Action(object):
        EXECUTE = 'exec'
        FILL = 'fill'
        EDIT = 'edit'

    def __init__(self, lines, lines_capacity=0, search_string=''):
        self._lines = list(iter_unique(lines))
        self._search_chars = list(search_string)
        self._position = -1
        self._lines_capacity = lines_capacity
        self._action = None

    @property
    def search_string(self):
        return ''.join(self._search_chars)

    @property
    def matching_lines(self):
        return list(itertools.islice(
            iter_matching_lines(self._lines, self.search_string),
            self._lines_capacity,
        ))

    @property
    def num_of_matching_lines(self):
        return len(self.matching_lines)

    @property
    def best_matching_line(self):
        position = self._position if self._position >= 0 else 0
        try:
            return self.matching_lines[position]
        except IndexError:
            return None

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if self._action is not None:
            raise ValueError('Action already set')
        self._action = action

    @property
    def lines_capacity(self):
        return self._lines_capacity

    @lines_capacity.setter
    def lines_capacity(self, lines_capacity):
        self._lines_capacity = lines_capacity
        if self._position >= self._lines_capacity:
            self._clear_position()

    @property
    def position(self):
        return self._position

    def move_position_up(self):
        self._position += 1
        if self._position >= self.num_of_matching_lines:
            self._position = 0

    def move_position_down(self):
        self._position -= 1
        if self._position < 0:
            self._position = self.num_of_matching_lines - 1

    def remove_character(self):
        if self._search_chars:
            self._search_chars.pop()
        self._clear_position()

    def append_character(self, c):
        self._search_chars.append(c)

    def _clear_position(self):
        self._position = -1
