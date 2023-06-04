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


if __name__ == '__main__':
    application = create_app()
    application.run()
else:
    application = create_app()
