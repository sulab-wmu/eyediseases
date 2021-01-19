#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

import matplotlib

matplotlib.use("Agg")

import logging

from ek_optical.cli import create_flask_app

logger = logging.getLogger(__name__)

app = create_flask_app()
logger.info('Optical Data Server Ready')
