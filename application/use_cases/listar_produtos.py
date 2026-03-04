class ListarProdutosUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository
    
    def execute(self, id=None):
        if id:
            return self.produto_repository.buscar_por_id(id)
        return self.produto_repository.listar_todos()
