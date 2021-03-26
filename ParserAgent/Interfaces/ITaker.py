from abc import ABCMeta, abstractmethod

class ITaker(object):
    
    @abstractmethod
    def Take(self, url):
        pass


