from flask_jwt_extended import create_access_token

class UsuarioService:
    def __init__(self, usuario_repository):
        self.repo = usuario_repository

    def login(self, email, senha):
        usuario_model = self.repo.buscar_por_email(email)

        if not usuario_model:
            return None
        
        if usuario_model.senha == senha:
            
            token = create_access_token(identity=str(usuario_model.id))
            return token
            
        return None