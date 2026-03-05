import bcrypt
from domain.ports.hash_service import HashService

class HashService(HashService):
    def hash_senha(self, senha):
        senha = str(senha)
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
        return hash_bytes.decode('utf-8')

    def verifica_senha(self, senha, hash_armazenado):
        return bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))