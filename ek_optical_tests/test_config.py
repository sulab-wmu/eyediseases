#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import os
from unittest import TestCase

from flask import current_app

from config.settings import UnitTestConfig
from ek_optical import create_app
from ek_optical_tests.helpers import envtemp


class TestUnitTestConfig(TestCase):

    def test_app_is_testing(self):
        test_env_vars = {
            'SECRET_KEY': 'some_random_key',
            'DATABASE_URL': 'some_sqlalchemy_url',
        }
        test_config = UnitTestConfig(db_url='some_sqlalchemy_url')
        with envtemp(test_env_vars):
            app = create_app(test_config)
            self.assertTrue(app.config['SECRET_KEY'] == 'unittest_secret_key')
            self.assertTrue(app.config['TESTING'])
            self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
            self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == 'some_sqlalchemy_url')
            self.assertFalse(app.config['DEBUG_TB_ENABLED'])


class TestDevelopmentConfig(TestCase):
    def test_app_is_development(self):
        test_env_vars = {
            'SECRET_KEY': 'some_random_key',
            'DATABASE_URL': 'some_sqlalchemy_url',
        }
        with envtemp(test_env_vars):
            app = create_app('development')
            self.assertEqual(app.config['SECRET_KEY'], 'some_random_key')
            self.assertEqual(app.config['SECRET_KEY'], os.environ.get('SECRET_KEY'))
            self.assertFalse(app.config['TESTING'])
            self.assertIsNotNone(current_app)
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], os.environ.get('DATABASE_URL'))


class TestProductionConfig(TestCase):
    def test_app_is_production(self):
        test_env_vars = {
            'SECRET_KEY': 'some_random_key',
            'DATABASE_URL': 'some_sqlalchemy_url',
        }
        with envtemp(test_env_vars):
            app = create_app('production')
            self.assertTrue(app.config['SECRET_KEY'] == os.environ.get('SECRET_KEY'))
            self.assertFalse(app.config['TESTING'])
            self.assertFalse(app.config['DEBUG_TB_ENABLED'])
            self.assertIsNotNone(current_app)
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], os.environ.get('DATABASE_URL'))
