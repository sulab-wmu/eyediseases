#!/bin/bash
#
# Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
# All rights reserved.
#

if [[ "$EK_DEV_VENV_DIR" == "" ]]; then
  echo "Need to set EK_DEV_VENV_DIR environment variable"
  exit 1
fi
source $EK_DEV_VENV_DIR/ek_optical/bin/activate

export FLASK_CONFIG=development
export FLASK_ENV=development
export SECRET_KEY=my_precious
export DATABASE_URL='postgresql://localhost/optical'

flask "$@"
