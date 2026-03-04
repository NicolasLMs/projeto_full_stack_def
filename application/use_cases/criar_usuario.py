from domain.entities.usuario import Usuario

class CriarUsuarioUseCase:
    def __init__(self, usuario_repository, sms_service):
        self.usuario_repository = usuario_repository
        self.sms_service = sms_service
    
    def execute(self, nome, cnpj, email, celular, senha):
        usuario = Usuario(nome, cnpj, email, celular, senha)
        usuario_criado = self.usuario_repository.criar(usuario)
        
        try:
            self.sms_service.enviar_verificacao(celular)
        except Exception as e:
            # SMS falhou mas usuário foi criado
            print(f"Erro ao enviar SMS: {e}")
        
        return usuario_criado
