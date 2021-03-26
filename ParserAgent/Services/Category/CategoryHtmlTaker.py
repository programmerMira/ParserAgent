from Interfaces.ITaker import ITaker
from Interfaces.IObservable import IObservable
from Exceptions.NotFoundHtmlPageException import NotFoundHtmlPageException
import requests

class CategoryHtmlTaker(ITaker, IObservable):
    
    def __init__(self, parser):
        self.__parser = parser

    def Take(self, url):
        response = requests.get(url)
        if(response.status_code == 200):
            self.NotifyObservers(response.content)
        elif(response.status_code == 404):
            raise NotFoundHtmlPageException(self.__notFoundExceptionMessage, str(type(self).__name__))

    def RegisterObserver(self, observer):
        self.__observers.append(observer)

    def RemoveObserver(self, observer):
        self.__observers.remove(observer)

    def NotifyObservers(self,data):
        for observer in self.__observers:
            observer.Update(self.__parser.Pars(data))
    
    __observers = list()
    __parser = None
    __notFoundExceptionMessage = "Запрашиваемый URL не найден"

