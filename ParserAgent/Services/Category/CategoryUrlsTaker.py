from Interfaces.ITaker import ITaker
from Interfaces.IObservable import IObservable
import requests
from Exceptions.NotFoundHtmlPageException import NotFoundHtmlPageException
from bs4 import BeautifulSoup

class CategoryUrlsTaker(ITaker, IObservable):

    def __init__(self):
        pass

    def Take(self, url):
        data = self.__getUrlData(url)
        main_categories = self.__getMainCategories(url,data)
        sub_categories = []
        for cat in main_categories:
            data = self.__getUrlData(cat['url'])
            if(data):
                found_subCats=self.__getSubCategories(url,data, cat['title'])
                if(len(found_subCats)>0):
                    sub_categories.append(found_subCats)
        self.NotifyObservers(sub_categories)
        #returns only subcategories 'cause main ones' don`t have products in it
        

    def __getUrlData(self,url):
        try:
            response = requests.get(url)
            if(response.status_code == 200):
                return response.content
            elif(response.status_code == 404):
                raise NotFoundHtmlPageException(self.__notFoundExceptionMessage.format(str(type(self).__name__)))
        except:
            print("Not valid url:",url)
            return None

    def __getMainCategories(self, url, data):
        soup = BeautifulSoup(data, 'lxml')
        cats = soup.find_all('li','topmenus-item')
        res = []
        for cat in cats:
            tmp = cat.find('a')
            res.append({
                'title':tmp.text,
                'url':url+tmp.get('href')
            })
        return res
    
    def __getSubCategories(self, url, data, mainCategoryTitle):
        soup = BeautifulSoup(data, 'lxml')
        res = []
        tmp_cats = soup.find('ul','maincatalog-list-2')
        if(tmp_cats):
            cats = tmp_cats.find_all('a')
            for cat in cats:
                res.append({
                    'main_title':mainCategoryTitle,
                    'title':cat.text,
                    'url':url+cat.get('href')
                })
        return res

    def RegisterObserver(self, observer):
        self.__observers.append(observer)

    def RemoveObserver(self, observer):
        self.__observers.remove(observer)

    def NotifyObservers(self,data):
        for observer in self.__observers:
            observer.Update(data)
    
    __observers = list()