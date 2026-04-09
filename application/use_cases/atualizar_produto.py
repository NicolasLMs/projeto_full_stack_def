class AtualizarProdutoUseCase:
    def __init__(self, produto_repository):
        self.produto_repository = produto_repository
    
    def execute(self, nome, preco, quantidade, id_usuario, imagem=None):
        produto = self.produto_repository.listar_todos(id)
        if not produto:
            raise ValueError('Produto não encontrado')
        
        if nome is not None:
            produto.nome = nome
        if preco is not None:
            produto.preco = preco
        if quantidade is not None:
            produto.quantidade = quantidade
        if id_usuario is not None:
            produto.id_usuario = self.hash_service.hash_id_usuario(id_usuario)
        if imagem is not None:
            produto.email = imagem
        
        self.produto_repository.atualizar(produto)
        return produto
