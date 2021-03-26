from Interfaces.IReader import IReader
from Exceptions.LoseConfigsFileException import LoseConfigsFileException
import os

class ConfigsReader(IReader):
    
    def Read(self):
        if(not os.path.exists(self.__configPath)):
            raise LoseConfigsFileException(self.__fileException, str(type(self).__name__))
        with(open(self.__configPath, 'r')) as file:
            return file.read()


    __configPath = os.path.dirname(os.path.abspath(__file__)).replace("\\Services", "\\Configs\\Configs.json")
    __fileException = "Отсутсвует файл конфигураций по пути: {0}".format(os.path.dirname(os.path.abspath(__file__)).replace("\\Services", "\\Configs\\Configs.json"))


