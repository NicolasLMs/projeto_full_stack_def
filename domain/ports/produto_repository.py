from abc import ABC, abstractmethod

class ProdutoRepository(ABC):
    @abstractmethod
    def criar(self, produto):
        pass
    
    @abstractmethod
    def listar_todos(self):
        pass
    
    @abstractmethod
    def buscar_por_id(self, id):
        pass
