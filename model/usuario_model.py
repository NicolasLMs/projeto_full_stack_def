from model.model_banco import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable = False)
    cnpj = db.Column(db.String(14), nullable=False, unique = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(14), nullable = False)
    celular = db.Column(db.String(100), unique=False, nullable = False)
    status = db.Column(db.Boolean, default = False)