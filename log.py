# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


import logging
from typing import Optional
# from typing import Optional, Text, Dict, Any

# import re
# from logging import config as logging_config
# from time import time
# from contextlib import contextmanager

# from .config import C


class MetaLogger(type):
    def __new__(cls, name, bases, dict):
        wrapper_dict = logging.Logger.__dict__.copy()
        for key in wrapper_dict:
            if key not in dict and key != "__reduce__":
                dict[key] = wrapper_dict[key]
        return type.__new__(cls, name, bases, dict)


class QlibLogger(metaclass=MetaLogger):
    """
    Customized logger for Qlib.
    """

    def __init__(self, module_name):
        self.module_name = module_name
        # this feature name conflicts with the attribute with Logger
        # rename it to avoid some corner cases that result in comparing `str` and `int`
        self.__level = 0

    @property
    def logger(self):
        logger = logging.getLogger(self.module_name)
        logger.setLevel(self.__level)
        return logger

    def setLevel(self, level):
        self.__level = level

    def __getattr__(self, name):
        # During unpickling, python will call __getattr__. Use this line to avoid maximum recursion error.
        if name in {"__setstate__"}:
            raise AttributeError
        return self.logger.__getattribute__(name)


def get_module_logger(module_name, level: Optional[int] = None) -> logging.Logger:
    """
    Get a logger for a specific module.
    :param module_name: str
        Logic module name.
    :param level: int
    :return: Logger
        Logger object.
    """
    if level is None:
        # level = C.logging_level
        level = logging.INFO

    module_name = "qlib.{}".format(module_name)
    # Get logger.
    module_logger = QlibLogger(module_name)
    module_logger.setLevel(level)
    return module_logger

