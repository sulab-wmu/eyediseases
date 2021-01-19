#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os

from flask import Flask, jsonify
from flask.json import JSONEncoder as FlaskJSONEncoder
from werkzeug.middleware.proxy_fix import ProxyFix

from ek_optical.extensions import cors, db, toolbar, csrf, migrate
from ek_optical.util import InvalidUsage, make_dict_response, is_str, create_custom_json_encoder


def create_app(config_name_or_object=None):
    """
    Create a Flask application using the app factory pattern.

    :param config_name_or_object: can be 'development', 'production', 'default', or a configuration object.
    :return: Flask app
    """
    app = Flask(__name__)

    configure_app(app, config_name_or_object)
    configure_json_encoder(app)
    configure_middleware(app)
    configure_error_templates(app)
    configure_routes(app)
    configure_extensions(app)

    return app


def configure_json_encoder(app):
    app.json_encoder = create_custom_json_encoder(FlaskJSONEncoder)


def configure_app(app, config_name_or_object):
    if config_name_or_object is None:
        config_name_or_object = os.getenv('FLASK_CONFIG') or 'default'

    if is_str(config_name_or_object):
        from config.settings import config
        config_factory = config[config_name_or_object]
        relevant_config = config_factory()
        app.config.from_object(relevant_config)
        relevant_config.init_app(app)
    else:
        app.config.from_object(config_name_or_object)

    if 'APP_SETTINGS' in os.environ:
        app.config.from_envvar('APP_SETTINGS')


def configure_extensions(app):
    toolbar.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


def configure_routes(app):
    from ek_optical.genetics.api.gene import GeneAPI
    GeneAPI.register(app, route_base='/api/gene', trailing_slash=False)

    from ek_optical.variants.api.variant import VariantAPI
    VariantAPI.register(app, route_base='/api/variant', trailing_slash=False)

    from ek_optical.disease.api.disease import DiseasesAPI
    DiseasesAPI.register(app, route_base='/api/disease', trailing_slash=False)

    from ek_optical.expression.api.expression import ExpressionAPI
    ExpressionAPI.register(app, route_base='/api/expression', trailing_slash=False)

    from ek_optical.singlecell.api.singlecell import SingleCellAPI
    SingleCellAPI.register(app, route_base='/api/singleCell', trailing_slash=False)

    from ek_optical.epigenomics.api.epigenomics import EpigenomicsAPI
    EpigenomicsAPI.register(app, route_base='/api/epigenomics', trailing_slash=False)

    from ek_optical.misc.search import SearchAPI
    SearchAPI.register(app, route_base='/api/search', trailing_slash=False)

    from ek_optical.analysis.api.analysis import AnalysisAPI
    AnalysisAPI.register(app, route_base='/api/analysis', trailing_slash=False)


def configure_middleware(app):
    """
    Register 0 or more middleware (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # http://docs.gunicorn.org/en/stable/deploy.html
    # Swap request.remote_addr with the real IP address even if behind a proxy.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

    return None


def configure_error_templates(app):
    def resource_not_found(e):
        return jsonify({
            "code": '404',
            "title": '404 Not Found',
            "message": 'The requested URL was not found on the server.',
        }), 404

    def ratelimit_exceeded(e):
        return jsonify({
            "code": '429',
            "title": '429 Too Many Requests',
            "message": f'Rate limit exceeded: {e.description}',
        }), 429

    def handle_invalid_usage(error: InvalidUsage):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    def internal_server_error(e):
        return make_dict_response({
            "code": '500',
            "title": '500 Internal Server Error',
            "message": f'Internal Server Error: {e.description}',
        }, status_code=500)

    app.register_error_handler(404, resource_not_found)
    app.register_error_handler(429, ratelimit_exceeded)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(InvalidUsage, handle_invalid_usage)
