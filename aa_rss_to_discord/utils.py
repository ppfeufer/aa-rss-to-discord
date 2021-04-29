"""
utility functions
"""

import logging


class LoggerAddTag(logging.LoggerAdapter):
    """
    add custom tag to a logger
    """

    def __init__(self, my_logger, prefix):
        super().__init__(my_logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        """
        process log items
        :param msg:
        :type msg:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        return "[%s] %s" % (self.prefix, msg), kwargs
