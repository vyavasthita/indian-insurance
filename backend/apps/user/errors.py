"""Custom error handler.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file errors.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 4th Jun 2023

About; -
--------
    Custom error handlers for api requests.

Working; -
----------
    This module returns a custom error response when requested page is not found.

Uses; -
-------
    This is used by flask.

Reference; -
------------
    TBD
"""

from flask import jsonify
from apps import db, create_app
from utils.http_status import HttpStatus

app = create_app()
from flask import current_app

app_ctx = app.app_context()
app_ctx.push()

@app.errorhandler(HttpStatus.HTTP_404_NOT_FOUND)
def not_found_error(error) -> tuple:
    status_code = HttpStatus.HTTP_404_NOT_FOUND
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred.'
        }
    }

    return jsonify(response), status_code

@app.errorhandler(HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR)
def handle_unexpected_error(error) -> tuple:
    db.session.rollback()

    status_code = HttpStatus.HTTP_500_INTERNAL_SERVER_ERROR
    success = False
    response = {
        'success': success,
        'error': {
            'type': 'UnexpectedException',
            'message': 'An unexpected error has occurred.'
        }
    }

    return jsonify(response), status_code

@app.errorhandler(Exception)
def defaultHandler(e) -> tuple:
   return {}, e.code