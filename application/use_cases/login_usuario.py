from flask_jwt_extended import create_access_token

class LoginUseCase:
    def __init__(self, usuario_repository, hash_service):
        self.repo = usuario_repository
        self.hash_service = hash_service

    def execute(self, email, senha_plana):
        usuario_model = self.repo.buscar_por_email(email)

        if not usuario_model:
            return None
        
        senha_valida = self.hash_service.verifica_senha(senha_plana, usuario_model.senha)
        
        if senha_valida:
            token = create_access_token(identity=str(usuario_model.id))
            return token
            
        return None