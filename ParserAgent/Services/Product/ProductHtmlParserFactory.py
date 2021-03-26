from Interfaces.IFactory import IFactory
from Services.ProductHtmlParser import ProductHtmlParser
import threading

class ProductHtmlParserFactory(IFactory):
    
    def Create(self, *args):
        with self.__lock:
            return ProductHtmlParser(*args)

    __lock = threading.Lock()
