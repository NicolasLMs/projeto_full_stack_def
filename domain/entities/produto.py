class Produto:
    def __init__(self, nome, preco, quantidade, id_usuario, imagem=None, id=None, status=False):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.imagem = imagem
        self.id_usuario = id_usuario
