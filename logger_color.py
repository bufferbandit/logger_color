from __future__ import annotations

import logging
import sys

from config import LOGGING_FORMAT


class Colors:
    """Colors class:
    Reset all colors with colors.reset
    Two subclasses fg for foreground and bg for background.
    Use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    """
    RESET = "\033[0m"
    BOLD = "\033[01m"
    DISABLE = "\033[02m"
    UNDERLINE = "\033[04m"
    REVERSE = "\033[07m"
    STRIKETHROUGH = "\033[09m"
    INVISIBLE = "\033[08m"

    class fg:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHTGRAY = "\033[37m"
        DARKGRAY = "\033[90m"
        LIGHTRED = "\033[91m"
        LIGHTGREEN = "\033[92m"
        YELLOW = "\033[93m"
        LIGHTBLUE = "\033[94m"
        PINK = "\033[95m"
        LIGHTCYAN = "\033[96m"

    class bg:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        ORANGE = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        LIGHTGRAY = "\033[47m"


class CustomFormatter(logging.Formatter):
    def paint_in_fmt(self,

                     format_color: Colors.Fg | Colors.bg = Colors.RESET, message_color: Colors.Fg | Colors.bg = Colors.RESET):
        message_format = " %(message)s"
        return message_color + format_color + self.fmt.replace(message_format,
                                                               f"{Colors.RESET}{message_color}{message_format}{Colors.RESET}")

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.INFO: self.paint_in_fmt(Colors.fg.YELLOW, Colors.fg.BLUE),
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


handlers = [
    handler.setFormatter(CustomFormatter(LOGGING_FORMAT)) or handler
    if handler.__class__.__name__ == "StreamHandler"
    else handler for handler in
    [
        logging.FileHandler(filename="logfile.log"),
        logging.StreamHandler(sys.stdout)
    ]
]

logging.basicConfig(
    format=LOGGING_FORMAT,
    handlers=handlers,
    level=logging.INFO)
