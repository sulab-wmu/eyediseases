#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

# config reference
# http://flask.pocoo.org/docs/1.0/config/
# https://github.com/miguelgrinberg/flasky/blob/master/config.py#L80

import logging
import os

from ek_optical.util import configure_logging

logger = logging.getLogger(__name__)


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

    # SQL Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Print SQL statements

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024

    # Image tagger specific
    IMG_TAGGER_USE_GENERATED_IMAGES = bool(os.environ.get('IMG_TAGGER_USE_GENERATED_IMAGES')) or False

    @staticmethod
    def init_app(app):
        pass

    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY') or self.get_default_secret_key()

    def get_default_secret_key(self):
        if not self.TESTING:
            logger.warning('Using default secret key!!!')

        return '4091f0a5-27f6-4531-8c21-18896135e16f'


class UnitTestConfig(BaseConfig):
    """Testing configuration"""
    ENV = 'development'
    TESTING = True

    def __init__(self, db_url):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = db_url
        self.SECRET_KEY = 'unittest_secret_key'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    ENV = 'development'

    def __init__(self):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/optical'

    @staticmethod
    def init_app(app):
        log_level = app.config['LOG_LEVEL']
        configure_logging(log_level)
        app.logger.setLevel(log_level)
        logger.info('Using DEVELOPMENT configuration')


class ProductionConfig(BaseConfig):
    """Production configuration"""

    def __init__(self):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/optical'

    @staticmethod
    def init_app(app):
        log_level = app.config['LOG_LEVEL']
        configure_logging(log_level)
        app.logger.setLevel(log_level)
        logger.info('Using PRODUCTION configuration')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
