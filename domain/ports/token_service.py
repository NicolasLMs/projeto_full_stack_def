from abc import ABC, abstractmethod

class TokenService(ABC):

    @abstractmethod
    def gerar_token(self,id):
        pass
