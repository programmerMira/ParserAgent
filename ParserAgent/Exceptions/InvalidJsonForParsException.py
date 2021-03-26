class InvalidJsonForParsException(object):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000031. Ошибка сгенерирована классом {}. Message: {}".format(className, message)


