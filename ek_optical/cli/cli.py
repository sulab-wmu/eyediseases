#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os

from ek_optical.cli import create_flask_app
from ek_optical.extensions import db

CMD_FOLDER = os.path.join(os.path.dirname(__file__), 'commands')
CMD_PREFIX = 'cmd_'

app = create_flask_app()


@app.shell_context_processor
def ctx():
    return {
        'app': app,
        'db': db,
    }


def list_commands():
    """
    Obtain a list of all available commands.

    :param ctx: Click context
    :return: List of sorted commands
    """
    commands = []

    for filename in os.listdir(CMD_FOLDER):
        if filename.endswith('.py') and filename.startswith(CMD_PREFIX):
            commands.append(filename[4:-3])
    commands.sort()

    return commands


def get_single_command(name):
    filename = os.path.join(CMD_FOLDER, CMD_PREFIX + name + '.py')
    ns = {}
    with open(filename, mode='rt', encoding='utf-8') as f:
        code = compile(f.read(), filename, 'exec', )
        eval(code, ns, ns)

    return ns['cli']


def register_all_commands():
    for name in list_commands():
        cmd = get_single_command(name)
        app.cli.add_command(cmd, name=name.replace('_', '-'))


register_all_commands()
