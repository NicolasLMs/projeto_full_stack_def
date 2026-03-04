from abc import ABC, abstractmethod

class SmsService(ABC):
    @abstractmethod
    def enviar_verificacao(self, celular):
        pass
    
    @abstractmethod
    def verificar_codigo(self, celular, codigo):
        pass
