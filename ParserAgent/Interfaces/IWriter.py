from abc import ABCMeta, abstractmethod

class IWriter(object):
    """  Class for writing information  
        
     Open methods:
     Write
    """
    
    @abstractmethod
    def Write(self, data):
        """  Writing information
       
        Keywords arguments:
        data - data, wchich will be written

        """
        pass


