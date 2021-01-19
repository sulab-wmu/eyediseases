#!/bin/bash
#
# Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
# All rights reserved.
#

source $TS_APP_HOME/bin/ts_env.sh
source $TS_APP_HOME/python/bin/activate

cd $TS_APP_HOME/app

#pybabel compile -d ek_optical/translations
exec gunicorn -c "python:config.gunicorn" --reload --workers=4 app:app
