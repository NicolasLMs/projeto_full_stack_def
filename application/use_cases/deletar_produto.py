class DeletarProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository

    def execute(self, id):
        self.produto_repository.deletar(id)
