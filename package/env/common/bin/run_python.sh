#!/bin/bash
#
# Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
# All rights reserved.
#

source $TS_APP_HOME/bin/ts_env.sh
exec $TS_APP_HOME/python/bin/python -u "$@"
