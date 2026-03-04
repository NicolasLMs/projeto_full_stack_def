class ConfirmarCadastroUsuarioUseCase:
    def __init__(self, usuario_repository, sms_service):
        self.usuario_repository = usuario_repository
        self.sms_service = sms_service
    
    def execute(self, id, codigo_otp):
        usuario = self.usuario_repository.buscar_por_id(id)
        if not usuario:
            raise ValueError('Usuário não encontrado')
        
        verificado = self.sms_service.verificar_codigo(usuario.celular, codigo_otp)
        if verificado:
            usuario.status = True
            self.usuario_repository.atualizar(usuario)
            return True
        return False
