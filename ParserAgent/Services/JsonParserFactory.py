from Interfaces.IFactory import IFactory
from Services.JsonParser import JsonParser
import threading

class JsonParserFactory(IFactory):
    

    def Create(self, *args):
        with self.__lock:
            return JsonParser(*args)


    __lock = threading.Lock()


