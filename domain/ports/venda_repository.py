from abc import ABC, abstractmethod

class VendaRepository(ABC):
    @abstractmethod
    def criar(self, venda):
        pass

    @abstractmethod
    def listar_por_usuario(self, id_usuario):
        pass
