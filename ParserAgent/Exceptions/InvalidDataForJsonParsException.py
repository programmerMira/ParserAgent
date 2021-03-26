class InvalidDataForJsonParsException(object):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000030. Ошибка сгенерирована классом {}. Message: {}".format(className, message)


