class NotFoundSsrModelException(Exception):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000010. Ошибка сгенерирована классом {}. Message: {}".format(className, message)


