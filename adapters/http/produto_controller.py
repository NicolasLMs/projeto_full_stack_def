from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


class ProdutoController:
    def __init__(self, criar_produto_use_case, listar_produtos_use_case,
                 atualizar_produto_use_case, deletar_produto_use_case=None):
        self.criar_produto_use_case = criar_produto_use_case
        self.listar_produtos_use_case = listar_produtos_use_case
        self.atualizar_produto_use_case = atualizar_produto_use_case
        self.deletar_produto_use_case = deletar_produto_use_case

    # ── POST /api/products ────────────────────────────────────────────────────
    @jwt_required()
    def criar_produto(self):
        data = request.get_json()
        id_usuario = int(get_jwt_identity())
        try:
            produto = self.criar_produto_use_case.execute(
                nome=data.get('name') or data.get('nome'),
                preco=data.get('price') if data.get('price') is not None else data.get('preco'),
                quantidade=data.get('stock') if data.get('stock') is not None else data.get('quantidade'),
                id_usuario=id_usuario,
                imagem=data.get('image_url') or data.get('imagem')
            )
            return jsonify({'message': 'Produto cadastrado com sucesso'}), 201
        except Exception as e:
            return jsonify({'message': str(e)}), 400

    # ── GET /api/products ─────────────────────────────────────────────────────
    @jwt_required()
    def listar_produtos(self):
        id_usuario = int(get_jwt_identity())
        search = request.args.get('search', '').lower()

        produtos = self.listar_produtos_use_case.execute(id_usuario=id_usuario)

        result = []
        for p in produtos:
            if search and search not in (p.nome or '').lower():
                continue
            result.append(self._serialize(p))
        return jsonify(result)

    # ── GET /api/products/<id> ────────────────────────────────────────────────
    @jwt_required()
    def listar_produto_por_id(self, id):
        id_usuario = int(get_jwt_identity())
        produto = self.listar_produtos_use_case.execute(id_usuario=id_usuario, id=id)
        if produto:
            return jsonify(self._serialize(produto))
        return jsonify({'message': 'Produto não encontrado'}), 404

    # ── PUT /api/products/<id> ────────────────────────────────────────────────
    @jwt_required()
    def atualizar_produto(self, id):
        data = request.get_json()
        try:
            self.atualizar_produto_use_case.execute(
                id=id,
                nome=data.get('name') or data.get('nome'),
                preco=data.get('price') if data.get('price') is not None else data.get('preco'),
                quantidade=data.get('stock') if data.get('stock') is not None else data.get('quantidade'),
                status=data.get('status'),
                imagem=data.get('image_url') or data.get('imagem'),
                id_usuario=data.get('id_usuario')
            )
            return jsonify({'message': 'Produto atualizado com sucesso!'}), 200
        except ValueError as e:
            return jsonify({'message': str(e)}), 404
        except Exception as e:
            return jsonify({'message': 'Erro ao atualizar produto', 'details': str(e)}), 500

    # ── DELETE /api/products/<id> ─────────────────────────────────────────────
    @jwt_required()
    def deletar_produto(self, id):
        if self.deletar_produto_use_case:
            try:
                self.deletar_produto_use_case.execute(id)
                return jsonify({'message': 'Produto excluído'}), 200
            except ValueError as e:
                return jsonify({'message': str(e)}), 404
            except Exception as e:
                return jsonify({'message': str(e)}), 500
        # Fallback: marca como inativo se não houver use case de deleção
        try:
            self.atualizar_produto_use_case.execute(id=id, status='inativo')
            return jsonify({'message': 'Produto excluído'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    def _serialize(self, p):
        return {
            'id': p.id,
            'name': p.nome,
            'description': '',
            'price': p.preco,
            'stock': p.quantidade,
            'category': 'outros',
            'sku': f'PROD-{p.id}',
            'image_url': p.imagem or '',
            'seller_id': p.id_usuario,
            'status': p.status,
            'created_at': '',
            'updated_at': '',
        }
