from Interfaces.IFactory import IFactory
from Services.CategoryHtmlTaker import CategoryHtmlTaker
import threading

class CategoryHtmlTakerFactory(IFactory):
   
    def Create(self, *args):
        with self.__lock:
            return CategoryHtmlTaker(*args)


    __lock = threading.Lock()