class Usuario:
    def __init__(self, nome, cnpj, email, celular, senha, id=None, status=False):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha
        self.status = status
