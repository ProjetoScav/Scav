from abc import ABC, abstractmethod


class Filtro(ABC):
    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def filtrar(self, query): ...
