from Interfaces.IParser import IParser
from Exceptions.InvalidDataForJsonParsException import InvalidDataForJsonParsException
import json

class DataToJsonParser(IParser):
    
    def Pars(self, data):
        if data:
            try:
                return json.dumps(data)
            except Exception as e:
                raise InvalidDataForJsonParsException(self.__invalidDataForJsonParsException, str(type(self).__name__))
        return None


    __invalidDataForJsonParsException = "Неправильный формат данных для парсинга в JSON"