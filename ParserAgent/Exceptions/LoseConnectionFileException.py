class LoseConnectionFileException(Exception):
    
    def __init__(self, message, className):
        self.__message = "Exception code: 000021. Ошибка сгенерирована классом {}. Message: {}".format(className, message)


