from model.usuario_model import db
from model.usuario_model import Usuario
import requests
from flask import request, jsonify
from twilio.rest import Client 
import os
from dotenv import load_dotenv

load_dotenv()


client = Client(os.getenv("account_sid"), os.getenv("auth_token"))


class usuario_controller:
    @staticmethod
    def criar_usuario():
        data = request.get_json()
        usuario = Usuario(
                nome = data.get('nome'),
                cnpj = data.get('cnpj'),
                email = data.get('email'),
                celular = data.get('celular'),
                senha = data.get('senha')
            )
        db.session.add(usuario)
        db.session.commit()

        #return jsonify({'mensagem': 'Usuário cadastrado com sucesso'}),201
    
        client.verify.v2.services(os.getenv("auth_token_2")) \
            .verifications \
            .create(to=usuario.celular, channel='sms')
            
        return jsonify({
            'mensagem': 'Usuário salvo, mas aguardando verificação de SMS.',
            'id_usuario': usuario.id
        }), 201 
    

    @staticmethod
    def listar_usuario():
        usuario = Usuario.query.all()
        return jsonify([{
           'id' : usuario.id,
           'nome' : usuario.nome,
           'cnpj': usuario.cnpj,
           'email' : usuario.email,
           'celular' : usuario.celular,
           'status' : usuario.status
           } for usuario in usuario
           ])
    
    @staticmethod
    def confirmar_cadastro(id):
        usuario = Usuario.query.get(id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        data = request.get_json()
        codigo = data.get('codigo_otp')

        check = client.verify.v2.services(os.getenv("auth_token_2")) \
            .verification_checks \
            .create(to=usuario.celular, code=codigo)

        if check.status == 'approved':
            usuario.status = True
            db.session.commit()
            return jsonify({'mensagem': 'Conta ativada com sucesso!'}), 200
        
        return jsonify({'erro': 'Código inválido'}), 400


