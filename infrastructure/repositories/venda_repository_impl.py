from domain.ports.venda_repository import VendaRepository
from domain.entities.venda import Venda
from infrastructure.database.models import db, VendaModel

class VendaRepositoryImpl(VendaRepository):
    def criar(self, venda):
        try:
            venda_model = VendaModel(
                id_produto=venda.id_produto,
                id_usuario=venda.id_usuario,
                quantidade_vendida=venda.quantidade_vendida,
                preco_unitario=venda.preco_unitario,
                forma_pagamento=venda.forma_pagamento
            )
            db.session.add(venda_model)
            db.session.commit()
            venda.id = venda_model.id
            return venda
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Erro ao registrar venda: {str(e)}')

    def listar_por_usuario(self, id_usuario):
        vendas_model = VendaModel.query.filter_by(id_usuario=id_usuario).all()
        return [Venda(
            id=v.id,
            id_produto=v.id_produto,
            id_usuario=v.id_usuario,
            quantidade_vendida=v.quantidade_vendida,
            preco_unitario=v.preco_unitario,
            forma_pagamento=v.forma_pagamento
        ) for v in vendas_model]
