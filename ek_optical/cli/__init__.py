#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import matplotlib
matplotlib.use("Agg")

import os

from ek_optical import create_app


def create_flask_app():
    return create_app(os.getenv('FLASK_CONFIG') or 'default')
