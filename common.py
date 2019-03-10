from abc import abstractclassmethod, ABCMeta
from loguru import logger as log


class Module(metaclass=ABCMeta):

    class Status:
        DEFAULT = 0
        PREPARE = 1
        RUNNING = 2
        STOPPED = 3

    module_name = 'unnamed_module'
    status = Status.DEFAULT

    @abstractclassmethod
    def __init__(self, module_name):
        self.module_name = module_name.upper()

    @abstractclassmethod
    def start(self):
        log.info('Module<%s> started.' % self.module_name)

    @abstractclassmethod
    def stop(self):
        log.info('Module<%s> stopped.' % self.module_name)

    def set_status(self, status):
        self.status = status

    def is_healthy(self):
        return self.status == Module.Status.RUNNING
