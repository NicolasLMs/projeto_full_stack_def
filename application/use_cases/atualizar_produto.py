class AtualizarProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository
    
    def execute(self, id, nome=None, preco=None, quantidade=None, id_usuario=None, status=None, imagem=None):
        produto = self.produto_repository.buscar_por_id_sem_filtro(id)
        if not produto:
            raise ValueError('Produto não encontrado')
        
        if nome is not None:
            produto.nome = nome
        if preco is not None:
            produto.preco = preco
        if quantidade is not None:
            produto.quantidade = quantidade
        if id_usuario is not None:
            produto.id_usuario = id_usuario
        if imagem is not None:
            produto.imagem = imagem
        if status is not None:
            produto.status = status

        self.produto_repository.atualizar(produto)
        return produto
