from domain.entities.produto import Produto

class CriarProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository
    
    def execute(self, nome, preco, quantidade, id_usuario, imagem=None):
        produto = Produto(nome, preco, quantidade, id_usuario, imagem)
        return self.produto_repository.criar(produto)
