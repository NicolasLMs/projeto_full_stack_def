class ListarUsuariosUseCase:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository
    
    def execute(self):
        return self.usuario_repository.listar_todos()
