from Interfaces.IParser import IParser
from Exceptions.NotFoundSsrModelException import NotFoundSsrModelException
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class ProductHtmlParser(IParser):
    
    def __init__(self, dataToJsonParser, jsonParser):
        self.__jsonParser = jsonParser
        self.__dataToJsonParser = dataToJsonParser

    def Pars(self, data):
        dictionary = dict()
        soup = BeautifulSoup(data, 'lxml')
        ssrModel = self.__jsonParser.Pars(self.__parsSsrModel(soup))
        if(not ssrModel):
            raise NotFoundSsrModelException(self.__notFoundSsrModel, str(type(self).__name__))
        try:
            dataForFeedback = '{"imtId":' + str(ssrModel['productCard']['link']) + ',"skip":0,"take":20}'
            response = requests.post('https://public-feedbacks.wildberries.ru/api/v1/summary/full', data=dataForFeedback)
            if(response.status_code == 200):
                fullAboutFeedbacks = response.json()
            else: 
                fullAboutFeedbacks = None
        except Exception as e:
            fullAboutFeedbacks = None
        try:
            url = 'https://questions.wildberries.ru/api/v1/questions?imtId={}&skip=0&take=20'.format(ssrModel['productCard']['link'])      
            response = requests.get(url)
            if(response.status_code == 200):
                fullAboutQuestions = response.json()
            else:
                fullAboutQuestions = None
        except Exception as e:
            fullAboutQuestions = None
        try:
            url = 'https://www.wildberries.ru/recommendations/recommended-by-nm?nmId={}'.format(ssrModel['productCard']['link'])
            response = requests.get(url)
            if(response.status_code == 200):   
                recomended = response.json()
            else:
                recomended = None
        except Exception as e:
            recomended = None
        try:
            url = 'https://www.wildberries.ru/recommendations/similar-by-nm?nmId={}'.format(ssrModel['productCard']['link'])
            response = requests.get(url)
            if(response.status_code == 200):
                similar = response.json()
            else:
                similar = None
        except Exception as e:
            similar = None
        try:
            url = 'https://www.wildberries.ru/recommendations/also-buy-by-nm?nmId={}'.format(ssrModel['productCard']['link'])
            response = requests.get(url)
            if(response.status_code == 200):
                alsoBuy = response.json()
            else:
                alsoBuy = None
        except Exception as e:
            alsoBuy = None
        try:
            dictionary['article'] = self.__parsArticle(soup)
            url = 'https://www.wildberries.ru/spa/product/deliveryinfo?latitude=55,7247&longitude=37,7882&cityId=77' 
            response = requests.get(url)
            if(response.status_code == 200):
                deliveryStores = response.json()
            else:
                deliveryStores = None
        except Exception as e:
            deliveryStores = None
        try:
            url = 'https://nm-2-card.wildberries.ru/enrichment/v1/api?nm={}'.format('9177553')
            response = requests.get(url)
            if(response.status_code == 200):
                stock = response.json()
            else:
                stock = None
        except Exception as e:
            stock = None
        dictionary['title'] = self.__parsTitle(soup)
        dictionary['buyMost'] = self.__parsBuyMost(ssrModel, dictionary['article'])
        dictionary['price'] = self.__parsPrice(ssrModel)
        dictionary['priceWithoutDiscout'] = self.__parsPriceWithoutDiscount(ssrModel)
        dictionary['brand'] = self.__parsBrand(ssrModel)
        dictionary['vendor'] = self.__parsVendor(ssrModel, dictionary['article'])
        dictionary['deliveryDays'] = self.__parsDeliveryDaysQty(ssrModel, deliveryStores,dictionary['article'] )
        dictionary['photoQty'] = self.__parsPhotoQty(ssrModel, dictionary['article'])
        dictionary['videoFlag'] = self.__parsVideoExists(ssrModel, dictionary['article'])
        dictionary['productTitleLength'] = len(dictionary['title'])
        dictionary['productDescriptionLength'] = self.__parsProductDescriptionLength(ssrModel)
        dictionary['reviewWithPhotoQty'] = self.__parsReviewWithPhotoQty(fullAboutFeedbacks)
        dictionary['reviewWithFiveStarsQty'] = self.__parsReviewWithFiveStarsQty(fullAboutFeedbacks)
        dictionary['reviewWithFourStarsQty'] = self.__parsReviewWithFourStarsQty(fullAboutFeedbacks)
        dictionary['reviewWithThreeStarsQty'] = self.__parsReviewWithThreeStarsQty(fullAboutFeedbacks)
        dictionary['reviewWithTwoStarsQty'] = self.__parsReviewWithTwoStarsQty(fullAboutFeedbacks)
        dictionary['reviewWithOneStarsQty'] = self.__parsReviewWithOneStarsQty(fullAboutFeedbacks)
        dictionary['firstReviewDate'] = self.__parsFirstReviewDate(fullAboutFeedbacks)
        dictionary['answersOnReviewsQty'] = self.__parsAnswersOnReviewsQty(fullAboutFeedbacks)
        dictionary['questionsQty'] = self.__parsQuestionsQty(fullAboutQuestions)
        dictionary['answersOnQuestionsQty'] = self.__parsAnswersOnQuestionsQty(fullAboutQuestions)
        dictionary['recomendedUrls'] = self.__parsRecomendedUrls(recomended)
        dictionary['advertisingUrls'] = self.__parsAdvertisingUrls(ssrModel)
        dictionary['similarUrls'] = self.__parsSimilarUrls(similar)
        dictionary['buyWithProductUrls'] = self.__parsBuyWithProductUrls(alsoBuy)
        dictionary['findWithThisProductKeyWords'] = self.__parsFindWithThisProductKeyWords(ssrModel)
        dictionary['stock'] = self.__parsStock(stock)
        return self.__dataToJsonParser.Pars(dictionary)

    def __parsSsrModel(self, data):
        for script in data.find_all('script'):
            if(script.next.find('ssrModel') != -1):
                startIndex = script.next.find('ssrModel')
                endIndex = script.next.find('seoHelper')
                if(startIndex != -1 and endIndex != -1):
                    return script.next[startIndex + 10:endIndex - 29].replace('\\"', 'JSON')

    def __parsArticle(self, data):
        tmp_data = data.find('div', 'article')
        if(tmp_data):
            return tmp_data.find('span').next
        return None

    def __parsTitle(self, data):
        tmp_data = data.find('span', 'name')
        if(tmp_data):
            return tmp_data.next
        return None

    def __parsBuyMost(self, data, article):
        if(not article):
            return None
        try:
            return data['nomenclatures'][article]['ordersCount']
        except Exception as e:
            return None

    def __parsPrice(self, data):
        try:
            return data['priceForProduct']['priceWithSale']
        except Exception as e:
            return None

    def __parsPriceWithoutDiscount(self, data):
        try:
            return data['priceForProduct']['price']
        except Exception as e:
            return None

    def __parsBrand(self, data):
        try:
            return data['productCard']['brandName']
        except Exception as e:
            return None

    def __parsVendor(self, data, article):
        if(not article):
            return None
        try:
            return data['suppliersInfo'][article]['supplierName']
        except Exception as e:
            return None

    def __parsDeliveryDaysQty(self, data, deliveryStores, article):
        if(not deliveryStores or not article):
            return None
        try:
            stores = data['productCard']['nomenclatures'][article]['sizes'][0]['storeIds']
            dates = list()
            for store in stores:
                for info in deliveryStores['value']['times']:
                    if(info['storeId'] == store):
                        dates.append(info['closestDeliveryDate'])
            result = 1000
            for date in dates:
                tmp = date + "Z"
                time = datetime.strptime(tmp, "%Y-%m-%dT%H:%M:%S.%fZ")
                if(result != None and time.day - datetime.today().day < result):
                    result = time.day - datetime.today().day
            return result
        except Exception as e:
            return None

    def __parsPhotoQty(self, data, article):
        if(not article):
            return None
        try:
            return data['nomenclatures'][article]['picsCount']
        except Exception as e:
            return None            

    def __parsVideoExists(self, data, article):
        if(not article):
            return None
        try:
            return data['nomenclatures'][article]['hasVideo']
        except Exception as e:
            return None           

    def __parsProductDescriptionLength(self, data):
        try:
            return len(data['productCard']['description'])
        except Exception as e:
            return None 

    def __parsReviewWithPhotoQty(self, data):
        if(not data):
            return None
        try:
            return data['feedbackCountWithPhoto']
        except Exception as e:
            return None 

    def __parsReviewWithFiveStarsQty(self, data):
        if(not data):
            return None
        try:
            return data['valuationDistribution']['5']
        except Exception as e:
            return None 

    def __parsReviewWithFourStarsQty(self, data):
        if(not data):
            return None
        try:
            return data['valuationDistribution']['4']
        except Exception as e:
            return None         

    def __parsReviewWithThreeStarsQty(self, data):
        if(not data):
            return None
        try:
            return data['valuationDistribution']['3']
        except Exception as e:
            return None 

    def __parsReviewWithTwoStarsQty(self, data):
        if(not data):
            return None
        try:
            return data['valuationDistribution']['2']
        except Exception as e:
            return None 

    def __parsReviewWithOneStarsQty(self, data):
        if(not data):
            return None
        try:
            return data['valuationDistribution']['1']
        except Exception as e:
            return None 

    def __parsFirstReviewDate(self, data):
        if(not data):
            return None
        try:
            length = len(data['feedbacks'])
            if(length != 0):
                return data['feedbacks'][length-1]['createdDate']
        except Exception as e:
            return None 

    def __parsAnswersOnReviewsQty(self, data):
        if(not data):
            return None
        try:
            count = 0
            for feedback in data['feedbacks']:
                if (feedback['answer'] != None):
                    count = count + 1
            return count
        except Exception as e:
            return None 

    def __parsQuestionsQty(self, data):
        if(not data):
            return None
        try:
            return data['count']
        except Exception as e:
            return None 

    def __parsAnswersOnQuestionsQty(self, data):
        if(not data):
            return None
        try:
            count = 0
            if 'questions' in data:
                for feedback in data['questions']:
                    if (feedback['answer'] != None):
                        count = count + 1
            return count
        except Exception as e:
            return None

    def __parsRecomendedUrls(self, data):
        if(not data):
            return None
        try:
            return data['value']['nmIds']
        except Exception as e:
            return None

    def __parsAdvertisingUrls(self, data):
        pass

    def __parsStock(self, data):
        if(not data):
            return None
        try:
            tmp = []
            for i in data['data']['products'][0]['sizes'][0]['stocks']:
                tmp.append(i)
            return tmp
        except Exception as e:
            return None

    def __parsSimilarUrls(self, data):
        if(not data):
            return None
        try:
            if data['value']:
                return  data['value']['nmIds']
        except Exception as e:
            return None
        
    def __parsBuyWithProductUrls(self, data):
        if(not data):
            return None
        try:
            return data['value']['nmIds']
        except Exception as e:
            return None
        
    def __parsFindWithThisProductKeyWords(self, data):
        if(not data):
            return None
        try:
            words = list()
            for key in data['searchTags']['tagsViewModels']:
                words.append(key['text'])
            return words
        except Exception as e:
            return None


    __jsonParser = None
    __dataToJsonParser = None
    __notFoundSsrModel = "На странице товара нет ssrModel. Убедитесь в правильности исходной ссылки"
