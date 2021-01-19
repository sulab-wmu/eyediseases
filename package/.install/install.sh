#!/bin/bash
#
# Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
# All rights reserved.
#

set -o errexit

# Create python virtual environment
python3.6 -m venv $TS_APP_HOME/python

# Install bootstrap dependencies
$TS_APP_HOME/bin/run_pip.sh --upgrade pip==20.0.2
$TS_APP_HOME/bin/run_pip.sh --upgrade setuptools==46.1.3 wheel==0.34.2

# Install main application, dependencies are described by requirements.txt
$TS_APP_HOME/bin/run_pip.sh -r $TS_APP_HOME/app/requirements.txt
