from Interfaces.IRepository import IRepository
import os

class KeyWordsRepository(IRepository):
    """description of class"""

    def __init__(self):
        pass

    def Add(self, line):
        """ Adding new data in repository collection
       
        Keywords arguments:
        line - new data line

        """
        self.__data.append(line)

    def Clean(self):
        """ Cleaning repository """
        self.__data.clear()

    def DelDublicate(self):
        self.__data = list(set(self.__data))

    def Save(self):
         with open('text.txt', 'w') as f:
             for data in self.__data:
                 f.write("\n" + data)
             f.write("Key words count = {}".format( len(self.__data)))

    @property
    def Data(self):
        """ Get repository collection """
        return self.__data

    @Data.setter
    def Data(self, dataList):
        """ Set repository collection  """
        self.__data = dataList

    __data = list()
