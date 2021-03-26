from Interfaces.IParser import IParser
from Exceptions.InvalidJsonForParsException import InvalidJsonForParsException
import json

class JsonParser(IParser):
    """ Class for parsing json files """

    def Pars(self, data):
        if data:
            try:
                return json.loads(data)
            except:
                raise InvalidJsonForParsException(self.__invalidJsonForParsException, str(type(self).__name__))
        return None

    __invalidJsonForParsException = "Неправильный формат JSON для парсинга"


