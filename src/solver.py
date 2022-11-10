from typing import Set
from abc import ABC, abstractmethod

class Solver(ABC):

    @abstractmethod
    def question(self)->str:
        pass

    @abstractmethod
    def response(self, question:str, r1:int, r2:int, r3:int, r4:int, r5:int)->None:
        pass

    @abstractmethod
    def reset(self)->None:
        pass