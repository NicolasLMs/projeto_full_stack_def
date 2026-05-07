from abc import ABC, abstractmethod

class ProdutoRepository(ABC):
    @abstractmethod
    def criar(self, produto):
        pass
    
    @abstractmethod
    def listar_todos(self, id_usuario):
        pass
    
    @abstractmethod
    def buscar_por_id(self, id, id_usuario):
        pass

    @abstractmethod
    def buscar_por_id_sem_filtro(self, id):
        pass

    @abstractmethod
    def atualizar(self, produto):
        pass