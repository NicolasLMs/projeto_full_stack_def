class HistoricoVendasUseCase:
    def __init__(self, venda_repository):
        self.venda_repository = venda_repository

    def execute(self, id_usuario):
        return self.venda_repository.listar_por_usuario(id_usuario)
