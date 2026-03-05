from abc import ABC, abstractmethod

class UsuarioRepository(ABC):
    @abstractmethod
    def criar(self, usuario):
        pass
    
    @abstractmethod
    def listar_todos(self):
        pass
    
    @abstractmethod
    def buscar_por_email(self, email):
        pass
    
    @abstractmethod
    def atualizar(self, usuario):
        pass


