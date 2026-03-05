from flask_jwt_extended import create_access_token

class LoginUseCase:
    def __init__(self, usuario_repository):
        self.repo = usuario_repository

    def execute(self, email, senha):
        usuario = self.repo.login(email)

        if not usuario:
            return None

        if usuario.senha == senha:
            if usuario.status != True:

                raise ValueError("Conta ainda não ativada. Verifique seu SMS.")

            token = create_access_token(identity=str(usuario.id))
            return token
            
        return None