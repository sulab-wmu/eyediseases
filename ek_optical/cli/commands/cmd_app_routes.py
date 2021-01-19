#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import click
from flask import current_app as app
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def cli():
    """
    List all of the available routes.

    :return: str
    """
    output = {}

    for rule in app.url_map.iter_rules():
        route = {
            'path': rule.rule,
            'methods': '({0})'.format(', '.join(rule.methods))
        }

        output[rule.endpoint] = route

    endpoint_padding = max(len(endpoint) for endpoint in output.keys()) + 2

    for key in sorted(output):
        if 'debugtoolbar' not in key and 'debug_toolbar' not in key:
            click.echo('{0: >{1}}: {2}'.format(key, endpoint_padding, output[key]))
