#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
import sys

import config
from utils.colors import Colors


class CustomFormatter(logging.Formatter):
    def paint_in_fmt(self,
                     format_color: Colors.fg | Colors.bg = Colors.RESET,
                     message_color: Colors.fg | Colors.bg = Colors.RESET):
        message_format = "%(message)s"
        return message_color + format_color + self.fmt.replace(message_format,
                                                               f"{Colors.RESET}{message_color}{message_format}{Colors.RESET}")

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.INFO: self.paint_in_fmt(config.LOGGING_INFO_PATTERN_COLLOR,
                                            config.LOGGING_INFO_MSG_COLLOR),
            logging.ERROR: self.paint_in_fmt(config.LOGGING_ERROR_PATTERN_COLLOR,
                                             config.LOGGING_ERROR_MSG_COLLOR),
        }

    def format(self, record):
        # Set extra variable if not on record, in this case channel_id
        if not hasattr(record, "channel_id"):
            record.channel_id = ""
        log_fmt = self.fmt
        if self.colored:
            log_fmt = self.FORMATS[record.levelno]

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_formatted_colored(colored):
    formatter = CustomFormatter(config.LOGGING_FORMAT)
    formatter.colored = colored
    return formatter


handlers = [
    handler.setFormatter(get_formatted_colored(True)) or handler
    if handler.__class__.__name__ == "StreamHandler"
    else handler.setFormatter(get_formatted_colored(False)) or handler
    for handler in
    [
        logging.FileHandler(filename="logfile.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
]

logging.basicConfig(
    format=config.LOGGING_FORMAT,
    handlers=handlers,
    level=logging.INFO)
