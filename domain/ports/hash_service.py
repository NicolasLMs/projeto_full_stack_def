from abc import ABC, abstractmethod

class HashService(ABC):
    @abstractmethod
    def hash_senha(self,senha):
        pass

    @abstractmethod
    def verifica_senha(self,senha,hash_armazenado):
        pass