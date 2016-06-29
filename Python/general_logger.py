# -*- coding: utf-8 -*-

import logging
import logging.handlers
import sys
import threading
import os

__author__ = 'Ares Ou (aresowj@gmail.com)'

# public logging levels
LOG_LEVEL_NOTSET = logging.NOTSET
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_LEVEL_INFO = logging.INFO
LOG_LEVEL_WARNING = logging.WARNING
LOG_LEVEL_ERROR = logging.ERROR

# logger target
LOG_TARGET_CONSOLE = 0x1
LOG_TARGET_LOG_FILE = 0x10
LOG_TARGET_LOG_HTTP = 0x100


_LOGGER_FORMAT = "[%(levelname)7s] [%(asctime)s] [%(thread)d] [%(module)s] - %(message)s"


class InfoOrLessCritical(logging.Filter):
    def filter(self, record):
        return record.levelno < LOG_LEVEL_WARNING


class HandlerFactory(object):
    handlers = {}

    @classmethod
    def get_std_out_handler(cls):
        if 'std_out_handler' not in cls.handlers:
            std_out_handler = logging.StreamHandler(sys.stdout)
            std_out_handler.setFormatter(logging.Formatter(_LOGGER_FORMAT))
            std_out_handler.addFilter(InfoOrLessCritical())
            cls.handlers['std_out_handler'] = std_out_handler

        return cls.handlers['std_out_handler']

    @classmethod
    def get_std_err_handler(cls):
        if 'std_err_handler' not in cls.handlers:
            std_err_handler = logging.StreamHandler(sys.stderr)
            std_err_handler.setFormatter(logging.Formatter(_LOGGER_FORMAT))
            std_err_handler.setLevel(LOG_LEVEL_WARNING)
            cls.handlers['std_err_handler'] = std_err_handler

        return cls.handlers['std_err_handler']

    @classmethod
    def get_rotating_file_handler(cls, log_path, max_bytes, backup_count):
        if 'rotating_file_handler' not in cls.handlers:
            cls.handlers['rotating_file_handler'] = {}

        if log_path not in cls.handlers['rotating_file_handler']:
            rotating_file_handler = logging.handlers.RotatingFileHandler(
                log_path, 'a', max_bytes, backup_count)
            rotating_file_handler.setFormatter(logging.Formatter(_LOGGER_FORMAT))
            cls.handlers['rotating_file_handler'][log_path] = rotating_file_handler

        return cls.handlers['rotating_file_handler'][log_path]

# set root logger
logging.getLogger().setLevel(LOG_LEVEL_NOTSET)
logging.getLogger().addHandler(HandlerFactory.get_std_out_handler())
logging.getLogger().addHandler(HandlerFactory.get_std_err_handler())

# logger for this module
logger = logging.getLogger(__name__)


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class GeneralLogger(object):
    def __init__(self, level=LOG_LEVEL_DEBUG, log_by_thread=False, log_path='', max_bytes=0, backup_count=0):
        # default logger setting
        logger.info("General logger initializing...")
        self._loggers = {}
        self._log_level = level
        self._main_thread_id = str(self.get_current_thread_id())
        self._log_destination = LOG_TARGET_CONSOLE
        self._log_by_thread = log_by_thread
        self._log_path = log_path
        self._log_file_max_bytes = max_bytes
        self._log_file_backup_count = backup_count

    @staticmethod
    def get_current_thread_id():
        return threading.current_thread().ident

    @staticmethod
    def get_current_thread_name():
        return threading.current_thread().name

    def get_log_file_name(self):
        log_path = os.path.abspath(self._log_path)
        base_name = os.path.basename(log_path)
        base_dir = os.path.dirname(log_path)

        if self._log_by_thread:
            base_name = '%d_%s_%s' % (self.get_current_thread_id(), self.get_current_thread_name(), base_name)

        if os.path.isdir(log_path):
            # only folder path provided, create a name for the log file
            return os.path.join(log_path, base_name)
        elif base_name and '.' not in base_name:
            # path is like '/tmp/a' and folder should be created
            os.makedirs(log_path)
            return os.path.join(log_path, base_name)
        else:
            return os.path.join(base_dir, base_name)

    def get_logger(self):
        name = self._main_thread_id

        if self._log_by_thread:
            current_id = str(self.get_current_thread_id())

            if current_id != self._main_thread_id:
                # set loggers of sub threads as children of main logger
                # so that logs from sub thread will be processed by
                # main logger. Otherwise, main logs will not contain sub logs.
                name = self._main_thread_id + '.' + current_id

        if name not in self._loggers:
            self.set_logger(name)

        return self._loggers[name]

    def set_logger(self, name):
        if name not in self._loggers:
            new_logger = logging.getLogger(name)
            new_logger.setLevel(self._log_level)

            if self._log_path:
                # log path will vary if log by thread is enabled
                log_path = self.get_log_file_name()
                new_logger.addHandler(HandlerFactory.get_rotating_file_handler(
                    log_path, self._log_file_max_bytes, self._log_file_backup_count))

            self._loggers[name] = new_logger

    def set_log_path(self, file_path, max_bytes=0, backup_count=0):
        if isinstance(file_path, str):
            self._log_path = file_path
        if isinstance(max_bytes, int):
            self._log_file_max_bytes = max_bytes
        if isinstance(backup_count, int):
            self._log_file_backup_count = backup_count

    def set_log_level(self, new_level):
        self._log_level = new_level
        for instanceLogger in self._loggers.values():
            instanceLogger.setLevel(self._log_level)

    def set_log_by_thread_log(self, log_by_thread):
        self._log_by_thread = log_by_thread
        # if thread log is enabled, only enable the main logger
        for instanceLogger in self._loggers.values():
            instanceLogger.disabled = not self._log_by_thread

        try:
            self._loggers[self._main_thread_id].disabled = self._log_by_thread
        except KeyError:
            pass


def log_debug(message):
    GeneralLogger().get_logger().debug(message)


def log_info(message):
    GeneralLogger().get_logger().info(message)


def log_warning(message):
    GeneralLogger().get_logger().warning(message)


def log_error(message):
    GeneralLogger().get_logger().error(message)


if __name__ == '__main__':
    def worker(message):
        log_info(message + ' info')
        log_debug(message + ' debug')
        log_warning(message + ' warning')
        log_error(message + ' error')

    GeneralLogger().set_log_path('/tmp/test.txt')
    GeneralLogger().set_log_by_thread_log(True)
    GeneralLogger().set_log_level(LOG_LEVEL_DEBUG)
    log_debug('debug')
    log_warning('warning')
    log_info('info')
    log_error('error')
    t1 = threading.Thread(target=worker, args=('worker 1',))
    t2 = threading.Thread(target=worker, args=('worker 2',))
    t1.start()
    t2.start()
