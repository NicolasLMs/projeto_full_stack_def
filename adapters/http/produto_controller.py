from flask import request, jsonify
from flask_jwt_extended import jwt_required

class ProdutoController:
    def __init__(self, criar_produto_use_case, listar_produtos_use_case):
        self.criar_produto_use_case = criar_produto_use_case
        self.listar_produtos_use_case = listar_produtos_use_case
    
    @jwt_required()
    def criar_produto(self):
        data = request.get_json()
        produto = self.criar_produto_use_case.execute(
            nome=data.get('nome'),
            preco=data.get('preco'),
            quantidade=data.get('quantidade'),
            id_usuario=data.get('id_usuario'),
            imagem=data.get('imagem')
        )
        return jsonify({'mensagem': 'produto cadastrado com sucesso'}), 201
    
    @jwt_required()
    def listar_produtos(self, id=None):
        if id:
            produto = self.listar_produtos_use_case.execute(id)
            if produto:
                return jsonify({
                    'id': produto.id,
                    'nome': produto.nome,
                    'preco': produto.preco,
                    'quantidade': produto.quantidade,
                    'status': produto.status,
                    'imagem': produto.imagem,
                    'id_usuario': produto.id_usuario
                })
            return jsonify({'erro': 'Produto não encontrado'}), 404
        
        produtos = self.listar_produtos_use_case.execute()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'preco': p.preco,
            'quantidade': p.quantidade,
            'status': p.status,
            'imagem': p.imagem,
            'id_usuario': p.id_usuario
        } for p in produtos])
