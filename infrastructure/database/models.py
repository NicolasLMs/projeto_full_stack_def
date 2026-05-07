from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(100), unique=False, nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Usuário: {self.nome}, ID:{self.id}"

class ProdutoModel(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=False)
    imagem = db.Column(db.String(200), nullable=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    atividade = db.relationship('UsuarioModel', backref='produto')

    def __repr__(self):
        return f'Usuário: {self.nome}, ID: {self.id}'

class VendaModel(db.Model):
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(20), nullable=False, default='pix')
    produto = db.relationship('ProdutoModel', backref='vendas')
    usuario = db.relationship('UsuarioModel', backref='vendas')

    def __repr__(self):
        return f'Venda ID: {self.id}, Produto: {self.id_produto}'
