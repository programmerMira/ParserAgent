from abc import ABCMeta, abstractmethod

class IParser(object):
    
    @abstractmethod
    def Pars(self, data):
        pass


