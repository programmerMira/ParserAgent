from Interfaces.IFactory import IFactory
from Services.DataToJsonParser import DataToJsonParser
import threading

class DataToJsonParserFactory(IFactory):
    

    def Create(self, *args):
        with self.__lock:
            return DataToJsonParser(*args)


    __lock = threading.Lock()


