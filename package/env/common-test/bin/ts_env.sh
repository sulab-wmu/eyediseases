#!/bin/bash
#
# Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
# All rights reserved.
#

export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=optical
export PGUSER=optical
export PGPASSWORD=optical
export DATABASE_URL=postgresql://$PGUSER:$PGPASSWORD@$PGHOST:$PGPORT/$PGDATABASE
export SECRET_KEY=c2b33817-9d15-4f99-aa5e-ad4e9eb42711
export FLASK_CONFIG=development
