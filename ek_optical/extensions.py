#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

toolbar = DebugToolbarExtension()
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
csrf = CSRFProtect()
