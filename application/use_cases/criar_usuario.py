from domain.entities.usuario import Usuario

class CriarUsuarioUseCase:
    def __init__(self, usuario_repository, sms_service, hash_service):
        self.usuario_repository = usuario_repository
        self.sms_service = sms_service
        self.hash_service = hash_service
    
    def execute(self, nome, cnpj, email, celular, senha_plana):
        senha_hash = self.hash_service.hash_senha(senha_plana)
        
        usuario = Usuario(nome, cnpj, email, celular, senha_hash)
        
        usuario_criado = self.usuario_repository.criar(usuario)
        
        try:
            self.sms_service.enviar_verificacao(celular)
        except Exception as e:
            print(f"Erro ao enviar SMS: {e}")
        
        return usuario_criado