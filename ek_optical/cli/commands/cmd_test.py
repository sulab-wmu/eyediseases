#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('project', 'tests'))
def cli(path):
    """
    Run tests with Pytest.

    :param path: Test path
    :return: Subprocess call result
    """
    cmd = 'py.test {0}'.format(path)
    return subprocess.call(cmd, shell=True)
