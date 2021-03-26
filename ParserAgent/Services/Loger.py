from Interfaces.ILoger import ILoger
import os
from contextlib import closing
from datetime import datetime


class Loger(ILoger):
    """  Class for loging exceptions and actions  
        
        Open methods:
        Logg

        Interfaces:
        ILogger
    """
   
    def __init__(self, logPath):
        """ Init Logger object """
        if(os.path.exists(logPath)):
            self.__logFilePath = logPath + "\\Log.txt"
        else:
            if(not os.path.exists(os.path.dirname(os.path.abspath(__file__)).replace("\\Services", "\\Logering"))):
                os.mkdir(os.path.dirname(os.path.abspath(__file__)).replace("\\Services", "\\Logering"))
            self.__logFilePath = os.path.dirname(os.path.abspath(__file__)).replace("\\Services", "\\Logering\\Log.txt")

    def Log(self, text):
        """ Loging the text in the log file
       
        Keywords arguments:
        text - text wchich write in file

        """
        self.__file.write("\n"+ str(datetime.now()) + ": " + text)

    def OpenFile(self):
        self.__file = open(self.__logFilePath, "a")

    def CloseFile(self):
        self.__file.close()


    __logFilePath = ""
    __file = ""


