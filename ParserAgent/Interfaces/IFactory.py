from abc import ABCMeta, abstractmethod

class IFactory(object):

    @abstractmethod
    def Create(self, *args):
        pass

