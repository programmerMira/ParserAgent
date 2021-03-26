class NotFoundHtmlPageException(Exception):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000404. Ошибка сгенерирована классом {}. Message: {}".format(className, message)


