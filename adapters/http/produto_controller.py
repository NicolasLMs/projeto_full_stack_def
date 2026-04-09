from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProdutoController:
    def __init__(self, criar_produto_use_case, listar_produtos_use_case):
        self.criar_produto_use_case = criar_produto_use_case
        self.listar_produtos_use_case = listar_produtos_use_case
    
    @jwt_required()
    def criar_produto(self):
        data = request.get_json()
        id_usuario = int(get_jwt_identity())

        produto = self.criar_produto_use_case.execute(
            nome=data.get('nome'),
            preco=data.get('preco'),
            quantidade=data.get('quantidade'),
            id_usuario=id_usuario,
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

    @jwt_required()
    def atualizar_produto(self, id):
        data = request.get_json()
        try:
            self.atualizar_cadastro_use_case.execute(
                email=email,
                nome=data.get('nome'),
                cnpj=data.get('cnpj'),
                celular=data.get('celular'),
                senha=data.get('senha'),
                novo_email=data.get('email')
            )
            return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200
        except ValueError as e:
            return jsonify({'erro': str(e)}), 404
        except Exception as e:
            return jsonify({'erro': 'Erro ao atualizar usuário', 'detalhes': str(e)}), 500
