from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(14), nullable=False)
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
