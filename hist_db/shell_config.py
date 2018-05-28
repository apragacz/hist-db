from __future__ import absolute_import, print_function, unicode_literals
from string import Template

SHELL_CONFIG_TEMPLATE = r"""
shopt -s histappend
export HISTFILESIZE=${HISTFILESIZE}
export HISTSIZE=${HISTSIZE}
export HISTCONTROL=ignoreboth
export HISTIGNORE='${HISTIGNORE}'
# Append to history file, clear the history and re-read the history file
PROMPT_COMMAND='history -a ; history -c ; history -r; $$PROMPT_COMMAND'

if which hist-db > /dev/null; then
    function _hist_db_append() { (hist-db append &) }
    PROMPT_COMMAND='_hist_db_append ; history -a ; history -c ; history -r; $$PROMPT_COMMAND'
fi

if [[ $$- =~ .*i.* ]]; then
    if which hist-db > /dev/null; then
        bind '"\C-r": "\C-a hist-db search --reverse -- \C-j"'
    fi
fi
"""  # noqa: E501

HISTSIZE = 100000
HISTFILESIZE = HISTSIZE
IGNORED_COMMANDS = ('ls', 'bg', 'fg', 'history', 'pwd')
HISTIGNORE = ':'.join(IGNORED_COMMANDS)


def show_shell_config(config):
    template = Template(SHELL_CONFIG_TEMPLATE.lstrip())
    shell_config = template.substitute(
        HISTSIZE=HISTSIZE,
        HISTFILESIZE=HISTFILESIZE,
        HISTIGNORE=HISTIGNORE,
    )
    print(shell_config)
