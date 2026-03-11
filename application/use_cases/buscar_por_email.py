class Buscar_por_EmailUsuarioUseCase:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository
    
    def execute(self, email):
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario:
            raise ValueError('Usuário não encontrado')
        return self.usuario_repository.buscar_por_email(email)