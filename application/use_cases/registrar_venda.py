from domain.entities.venda import Venda

class RegistrarVendaUseCase:
    def __init__(self, venda_repository, produto_repository, usuario_repository):
        self.venda_repository = venda_repository
        self.produto_repository = produto_repository
        self.usuario_repository = usuario_repository

    def execute(self, id_produto, quantidade_vendida, id_usuario, forma_pagamento='pix'):
        # Valida dados de entrada
        if not id_produto or not isinstance(id_produto, int) or id_produto <= 0:
            raise ValueError('id_produto deve ser um inteiro positivo')
        if not quantidade_vendida or not isinstance(quantidade_vendida, int) or quantidade_vendida <= 0:
            raise ValueError('A quantidade vendida deve ser maior que zero')

        # Valida status do seller
        seller = self.usuario_repository.buscar_por_id(id_usuario)
        if not seller:
            raise PermissionError('Seller não encontrado')
        if not seller.status:
            raise PermissionError('Seller inativo não pode realizar vendas')

        # Busca o produto sem filtro de dono (venda pode ser de qualquer produto ativo)
        produto = self.produto_repository.buscar_por_id_sem_filtro(id_produto)
        if not produto:
            raise LookupError('Produto não encontrado')
        if not produto.status:
            raise ValueError('Produto inativo não pode ser vendido')
        if quantidade_vendida > produto.quantidade:
            raise ValueError('Quantidade vendida superior ao estoque disponível')

        # Registra a venda com o preço atual
        venda = Venda(
            id_produto=id_produto,
            id_usuario=id_usuario,
            quantidade_vendida=quantidade_vendida,
            preco_unitario=produto.preco,
            forma_pagamento=forma_pagamento
        )
        venda = self.venda_repository.criar(venda)

        # Atualiza o estoque
        produto.quantidade -= quantidade_vendida
        self.produto_repository.atualizar(produto)

        return venda
