from model.model_banco import db


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(30), nullable = False)
    preco = db.Column(db.Float, nullable = False)
    quantidade = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Boolean, default = False)
    imagem = db.Column(db.String(200), nullable = True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable = False)
    atividade = db.relationship('Usuario', backref='produto')

