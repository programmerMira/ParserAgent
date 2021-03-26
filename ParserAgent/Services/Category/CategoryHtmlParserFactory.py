from Interfaces.IFactory import IFactory
from Services.CategoryHtmlParser import CategoryHtmlParser
import threading

class CategoryHtmlParserFactory(IFactory):
    
    def Create(self, *args):
        with self.__lock:
            return CategoryHtmlParser(args[0], args[1])

    __lock = threading.Lock()
