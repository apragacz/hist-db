from __future__ import absolute_import, print_function, unicode_literals


def iter_unique(iterator):
    lines_directory = set()
    for line in iterator:
        if line in lines_directory:
            continue
        lines_directory.add(line)
        yield line


def iter_matching_lines(iterator, search_string):
    for line in iterator:
        if search_string not in line:
            continue
        yield line


def pad_with_spaces(text, width):
    trimmed_text = text.rstrip()[:width]
    trimmed_text_len = len(trimmed_text)
    padded_text = trimmed_text + (' ' * max(0, width - trimmed_text_len))
    assert len(padded_text) == width
    return padded_text
