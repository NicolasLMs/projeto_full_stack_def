from model.model_banco import db
from model.produtos_model import Produto
from flask import request, jsonify
import requests


class produto_controller:
    @staticmethod
    def criar_produto():
        data = request.get_json()
        produto = Produto(
            nome = data.get('nome'),
            preco = data.get('preco'),
            quantidade = data.get('quantidade'),
            imagem = data.get('imagem'),
            id_usuario = data.get('id_usuario'))
        
        db.session.add(produto)
        db.session.commit()
        return jsonify({'mensagem': 'produto cadastrado com sucesso'}),201 
    


    @staticmethod
    def listar_produtos():
        produtos = Produto.query.all()
        return jsonify([{
            'id': p.id,
            'nome': p.nome,
            'preco' : p.preco,
            'quantidade' : p.quantidade,
            'status' : p.status,
            'imagem' : p.imagem,
            'id_usuario' : p.id_usuario
        } for p in produtos])
    
    @staticmethod
    def lista_produto_id(id):
        produto = Produto.get(id)
        if produto:
            return jsonify({
                "id" : id,
                "nome" : produto.nome,
                "preco" : produto.preco,
                "quantidade" : produto.quantidade,
                "status" : produto.status,
                "imagem" : produto.imagem,
                "id_usuario" : produto.id_usuario
            })
