"""
Custom logging script
"""

import logging

DEBUG = False
DEBUG_DISCORD = False


def get_logger(name):
    """Function to get a logger
    Useful for modules that have already initialized a logger, such as discord.py
    """

    # Variables prefixed with __ are private

    __logger = logging.getLogger(name)
    __logger.setLevel(logging.DEBUG if DEBUG_DISCORD else logging.INFO)
    __ch = logging.StreamHandler()
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger


def init(name="root"):
    """Function to create a designated logger for separate modules"""

    # Variables prefixed with __ are private

    __logger = logging.Logger(name)
    __ch = logging.StreamHandler()
    __ch.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    __ch.setFormatter(CustomFormatter())
    __logger.addHandler(__ch)
    return __logger


class CustomFormatter(logging.Formatter):
    """Custom formatter class"""

    green = "\x1B[32m"
    yellow = "\x1B[33m"  # Sometimes orange in dark mode
    red = "\x1B[31m"
    reset = "\x1B[0m"

    format = "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s"
    FORMATS = {
        logging.DEBUG: green + f"{reset}[%(asctime)s]{green}[%(levelname)-7s][%(name)-14s]{reset}[{red}%(lineno)4s{reset}] %(message)s" + reset,
        logging.INFO: green + f"{green}[%(asctime)s]{green}[%(levelname)-7s][%(name)-14s]{reset}[{red}%(lineno)4s{reset}] %(message)s" + reset,
        logging.WARNING: yellow + f"[%(asctime)s][%(levelname)-7s][%(name)-14s][{red}%(lineno)4s{reset}{yellow}] %(message)s" + reset,
        logging.ERROR: red + "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s" + reset,
        logging.CRITICAL: red +
        "[%(asctime)s][%(levelname)-7s][%(name)-14s][%(lineno)4s] %(message)s" + reset
    } if DEBUG else {
        logging.DEBUG: reset,
        logging.INFO: green + "[%(asctime)s][%(levelname)7s]" + reset + " %(message)s" + reset,
        logging.WARNING: yellow + "[%(asctime)s][%(levelname)7s] %(message)s" + reset,
        logging.ERROR: red + "[%(asctime)s][%(levelname)7s] %(message)s" + reset,
        logging.CRITICAL: red +
        "[%(asctime)s][%(levelname)7s] %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%I:%M.%S%p")
        return formatter.format(record)
