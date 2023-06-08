"""Main applicationo module

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file wsgi.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    Main module to start flask app

Working; -
----------
    This modules starts application

Uses; -
-------
    This module is used by webserver to start flask app

Reference; -
------------
    TBD
"""

from apps import create_app

app = create_app()

app.app_context().push()

from apps import celery

if __name__ == '__main__':
    app.run()
else:
    application = create_app()
