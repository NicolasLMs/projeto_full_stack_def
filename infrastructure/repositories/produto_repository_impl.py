from domain.ports.produto_repository import ProdutoRepository
from domain.entities.produto import Produto
from infrastructure.database.models import db, ProdutoModel

class ProdutoRepositoryImpl(ProdutoRepository):
    def criar(self, produto):
        produto_model = ProdutoModel(
            nome=produto.nome,
            preco=produto.preco,
            quantidade=produto.quantidade,
            imagem=produto.imagem,
            id_usuario=produto.id_usuario,
            status=produto.status
        )
        db.session.add(produto_model)
        db.session.commit()
        produto.id = produto_model.id
        return produto
    
    def listar_todos(self):
        produtos_model = ProdutoModel.query.all()
        return [Produto(
            nome=p.nome,
            preco=p.preco,
            quantidade=p.quantidade,
            id_usuario=p.id_usuario,
            imagem=p.imagem,
            id=p.id,
            status=p.status
        ) for p in produtos_model]
    
    def buscar_por_id(self, id):
        produto_model = ProdutoModel.query.get(id)
        if not produto_model:
            return None
        return Produto(
            nome=produto_model.nome,
            preco=produto_model.preco,
            quantidade=produto_model.quantidade,
            id_usuario=produto_model.id_usuario,
            imagem=produto_model.imagem,
            id=produto_model.id,
            status=produto_model.status
        )
