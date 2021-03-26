from Interfaces.IFactory import IFactory
from Services.ProductHtmlTaker import ProductHtmlTaker
import threading

class ProductHtmlTakerFactory(IFactory):
    
    def Create(self, *args):
        with self.__lock:
            return ProductHtmlTaker(*args)

    __lock = threading.Lock()
