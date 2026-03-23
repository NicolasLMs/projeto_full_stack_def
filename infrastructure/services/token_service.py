from flask_jwt_extended import create_access_token
from domain.ports.token_service import TokenService
from datetime import timedelta

class JWTService(TokenService):
    def gerar_token(self, id):
        return create_access_token(identity=id, expires_delta=timedelta(minutes=5))