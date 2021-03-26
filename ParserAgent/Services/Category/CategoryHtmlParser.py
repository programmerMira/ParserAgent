from Interfaces.IParser import IParser
from bs4 import BeautifulSoup

class CategoryHtmlParser(IParser):
    
    def __init__(self, dataToJsonParser, jsonParser):
        self.__dataToJsonParser = dataToJsonParser
        self.__jsonParser = jsonParser

    def Pars(self, data):
        soup = BeautifulSoup(data,'lxml')
        parsed_soup = soup.find_all('div','dtList-inner')
        if(not parsed_soup):
            print("No products available by current link")
            return None
        category_prods_list=[]
        for index, item in enumerate(parsed_soup):
            tmp_list=[]
            pageNumber = self.__parsPageNumber(soup)
            positionNumber = self.__parsPositionNumber(index)
            url = "https://www.wildberries.ru"+self.__parsURL(item)
            productTitle = self.__parsProductTitle(item)
            brand = self.__parsBrand(item)
            price = self.__parsPrice(item)
            priceWithDiscount = self.__parsPriceWithDiscount(item)
            newTag = self.__parsNewTag(item)
            adversingTag = self.__parsAdversingTag(item)
            actionTag = self.__parsActionTag(item)
            rating = self.__parsRating(item)
            reviewsQty = self.__parsReviewsQty(item)
            tmp_list={
                'pageNumber':pageNumber,
                'positionNumber':positionNumber,
                'url':url,
                'productTitle':productTitle,
                'brand':brand,
                'price':price,
                'priceWithDiscount':priceWithDiscount,
                'newTag':newTag,
                'advertisingTag':adversingTag,
                'actionTag':actionTag,
                'rating':rating,
                'reviewsQty':reviewsQty
            }
            if(tmp_list not in category_prods_list):
                category_prods_list.append(tmp_list)
        if(self.__categoryParserData):
            self.__categoryParserData += category_prods_list
        else:
            self.__categoryParserData = category_prods_list
        return category_prods_list

    def __parsPositionNumber(self, number):
        if(number>-1):
            if(self.__categoryParserData):
                return len(self.__categoryParserData)+number
            return number
        return None

    def __parsPageNumber(self, data):
        test = data.find('span','pagination-item')
        if(test):
            return test.text.replace('\n','')
        return None

    def __parsURL(self,data):
        test = data.find('a','ref_goods_n_p')
        if(test):
            return test.get('href')
        return None

    def __parsProductTitle(self, data):
        test = data.find('span','goods-name')
        if(test):
            return test.text
        return None

    def __parsBrand(self, data):
        test = data.find('strong','brand-name')
        if(test):
            return test.text.replace('/','').strip()
        return None

    def __parsPrice(self, data):
        test = data.find('span','price-old-block')
        if(test==None):
            test = data.find('div','catalog-product-card-price')
        if(test==None):
            test = data.find('div','catalog-product-card-original-price')
        if(test):
            return test.text.replace('\xa0','')
        return None

    def __parsPriceWithDiscount(self, data):
        test = data.find('ins','lower-price')
        if(test):
            return test.text.replace('\xa0','')[1:-1]
        return None

    def __parsNewTag(self, data):
        test = data.find('ins','noveltyImg')
        if(test):
            return test.text
        return None

    def __parsAdversingTag(self, data):
        test = data.find('p','promo-tip')
        if(test):
            return test.text
        return None

    def __parsActionTag(self, data):
        test = data.find('span','spec-actions-catalog')
        if(test):
            return test.text
        return None

    def __parsRating(self, data):
        test = data.find('span','star5')
        if(test):
            return '5'
        test = data.find('span','star4')
        if(test):
            return '4'
        test = data.find('span','star3')
        if(test):
            return '3'
        test = data.find('span','star2')
        if(test):
            return '2'
        test = data.find('span','star1')
        if(test):
            return '1'
        return '0'

    def __parsReviewsQty(self, data):
        test = data.find('span','dtList-comments-count')
        if(test):
            return test.text
        return None

    __dataToJsonParser = None
    __categoryParserData = None
