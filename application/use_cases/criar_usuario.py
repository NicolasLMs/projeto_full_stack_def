from domain.entities.usuario import Usuario

class CriarUsuarioUseCase:
    def __init__(self, usuario_repository, sms_service):
        self.usuario_repository = usuario_repository
        self.sms_service = sms_service
    
    def execute(self, nome, cnpj, email, celular, senha):
        usuario = Usuario(nome, cnpj, email, celular, senha)
        usuario_criado = self.usuario_repository.criar(usuario)
        self.sms_service.enviar_verificacao(celular)
        return usuario_criado
