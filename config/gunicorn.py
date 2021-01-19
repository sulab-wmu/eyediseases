#  Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
#  All rights reserved.

bind = '0.0.0.0:5001'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
timeout = '300'
workers = '5'
worker_class = 'gevent'
worker_connections = '1000'
