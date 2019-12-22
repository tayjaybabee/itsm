#!/usr/bin/env python3
"""Logger library for the ITSM application"""

import logging
from colorlog import ColoredFormatter


def setup_logger(callerName):
    """Return a logger with a default ColoredFormatter."""
    if not callerName:
        callerName = 'ITSMApp'
    else:
        callerName = 'ITSMApp' + '.' + '%s' % callerName
    formatter = ColoredFormatter(
        "%(bold_cyan)s%(asctime)-s%(reset)s%(log_color)s::%(name)-14s::%(levelname)-10s%(reset)s%(blue)s%(message)-s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'bold_cyan',
            'INFO':     'bold_green',
            'WARNING':  'bold_yellow',
            'ERROR':    'bold_red',
            'CRITICAL': 'bold_red',
        }
    )

    logger = logging.getLogger(callerName)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info(f'Logger started for %s' % callerName)

    return logger

