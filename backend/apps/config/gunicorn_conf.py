"""Gunicorn Configuration.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file gunicorn_conf.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    Gunicorn configuration is done here.

Working; -
----------
    This class reads the no of cors and accordingly creates workers.

Uses; -
-------
    Gunicorn web server uses this configuration.

Reference; -
------------
    TBD
"""

import multiprocessing


loglevel = 'info'
errorlog = "-"
accesslog = "-"

bind = '0.0.0.0:5000'

workers = multiprocessing.cpu_count()

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True