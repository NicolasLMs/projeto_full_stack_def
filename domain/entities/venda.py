class Venda:
    def __init__(self, id_produto, quantidade_vendida, preco_unitario, id_usuario, forma_pagamento='pix', id=None):
        self.id = id
        self.id_produto = id_produto
        self.id_usuario = id_usuario
        self.quantidade_vendida = quantidade_vendida
        self.preco_unitario = preco_unitario
        self.forma_pagamento = forma_pagamento
