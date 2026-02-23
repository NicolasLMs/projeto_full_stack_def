import flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from controller.usuario_controller import usuario
from controller.produto_controller import produto
from model.model_banco import db

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'meu_banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

usuario(app)
produto(app)

if __name__ == '__main__':
    app.run(debug=True)