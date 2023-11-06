"""Http Status codes
SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file http_status.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 3rd Jun 2023

About; -
--------
    Module for HTTP status codes.

Working; -
----------
    This modules defines constants for HTTP status codes.

Uses; -
-------
    All modules use HTTP status codes from this module.

Reference; -
------------
    TBD
"""

class HttpStatus:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED =202
    HTTP_204_NO_CONTENT =204
    HTTP_400_BAD_REQUEST = 400
    HTTP_404_NOT_FOUND = 404
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_500_INTERNAL_SERVER_ERROR = 500