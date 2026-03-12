from flask_jwt_extended import create_access_token

class LoginUseCase:
    def __init__(self, usuario_repository, hash_service):
        self.repo = usuario_repository
        self.hash_service = hash_service

    def execute(self, email, senha):

        usuario = self.repo.buscar_por_email(email)

        if not usuario:
            return "Usuário não localizado"
        
        if usuario.status is not True:
            return "Conta inativa ou pendente de verificação."
        
        senha_str = str(senha)
        senha_valida = self.hash_service.verifica_senha(senha_str, usuario.senha)
        
        if senha_valida:
            token = create_access_token(identity=str(usuario.id))
            return token
            
        return None