"""Logging wrapper to provide single object for logging.

SENECA GLOBAL CONFIDENTIAL & PROPRIETARY

@file insurance_logger.py
@author Dilip Kumar Sharma
@copyright Seneca Global
@date 4th Jun 2023

About; -
--------
    It is responsible for creating single object of python logging module.

Design Pattern; -
-----------------
    This module is implemented using Singleton design pattern.

Working; -
----------
    Logging information is read from logging configuration file.
    This module exposes some static methods to write log information.

Uses; -
-------
    All other python modules will use this singleton object to write log information.

    Having single object for logging makes sure all log information are written to same log file.

    We initialize this singleton object at the beginning of running the application.

Reference; -
------------
    TBD
"""

import os
import logging
import logging.config
from apps import configuration


class InsuranceLogger:
    """ Class InsuranceLogger is a Singleton class used for creating single object
        to be used by python modules to log information.

        Having single object for logging makes sure all log information are written
        to same log file of matching server.

        Many python modules write log information and they need to write such
        information in the same log file. Hence we need a single object for  logging.

    Args:
        Not Applicable.
    Returns:
        Not Applicable.
    Raises:
        Not Applicable.
    """
    __instance = None

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if InsuranceLogger.__instance is None:
            InsuranceLogger()

        return InsuranceLogger.__instance

    def __init__(self):
        """ 
        Virtual private constructor.
        To restrict user using below way of creating class object.
        
        ob_1 = DSMigrationLogger()
        ob_2 = DSMigrationLogger()
        """
        if InsuranceLogger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            InsuranceLogger.__instance = self

            self.initialize_logging()
            
            self.logger = logging.getLogger(__name__)
    
    def initialize_logging(self):
        """ Initializes logging.
        
        Sets the logging file path, logging format and log level.
        
        Args:
            Not Applicable.
        Returns:
            Not Applicable.
        Raises:
            Not Applicable.
        """
        logging.config.fileConfig(
            fname=configuration.LOG_CONFIG_FILE, 
            disable_existing_loggers=False, 
            defaults={'log_file_name' : os.path.join(configuration.LOGS_DIR, configuration.LOG_FILE_NAME)}
        )

    @staticmethod
    def log_debug(log_message):
        InsuranceLogger.get_instance().logger.debug(log_message)

    @staticmethod
    def log_info(log_message):
        InsuranceLogger.get_instance().logger.info(log_message)

    @staticmethod
    def log_warning(log_message):            
        InsuranceLogger.get_instance().logger.warn(log_message)

    @staticmethod
    def log_error(log_message, exc_info=False):
        InsuranceLogger.get_instance().logger.error(log_message, exc_info=exc_info)

    @staticmethod
    def log_critical(log_message, exc_info=False):
        InsuranceLogger.get_instance().logger.critical(log_message, exc_info=exc_info)