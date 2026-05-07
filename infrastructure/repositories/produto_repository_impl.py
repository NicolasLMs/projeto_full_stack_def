from domain.ports.produto_repository import ProdutoRepository
from domain.entities.produto import Produto
from infrastructure.database.models import db, ProdutoModel

class ProdutoRepositoryImpl(ProdutoRepository):
    def criar(self, produto):
        try:
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
        except Exception as e:
            db.session.rollback()
            raise ValueError('Erro ao cadastrar produto')
    
    def listar_todos(self, id_usuario):
        produtos_model = ProdutoModel.query.filter_by(id_usuario=id_usuario).all()
        return [Produto(
            nome=p.nome,
            preco=p.preco,
            quantidade=p.quantidade,
            id_usuario=p.id_usuario,
            imagem=p.imagem,
            id=p.id,
            status=p.status
        ) for p in produtos_model]
    
    def buscar_por_id(self, id, id_usuario):
        produto_model = ProdutoModel.query.filter_by(id=id, id_usuario=id_usuario).first()
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
    
    def buscar_por_id_sem_filtro(self, id):
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

    def atualizar(self, produto):
        produto_model = ProdutoModel.query.get(produto.id)

        if not produto_model:
            raise ValueError('Produto não encontrado')

        try:
            produto_model.nome = produto.nome
            produto_model.preco = produto.preco
            produto_model.quantidade = produto.quantidade
            produto_model.imagem = produto.imagem
            produto_model.status = produto.status
            produto_model.id_usuario = produto.id_usuario
            db.session.commit()

            return produto

        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Erro ao atualizar produto: {str(e)}')

    def deletar(self, id):
        produto_model = ProdutoModel.query.get(id)
        if not produto_model:
            raise ValueError('Produto não encontrado')
        try:
            db.session.delete(produto_model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f'Erro ao deletar produto: {str(e)}')