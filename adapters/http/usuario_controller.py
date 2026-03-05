from flask import request, jsonify
from flask_jwt_extended import jwt_required

class UsuarioController:
    def __init__(self, criar_usuario_use_case, listar_usuarios_use_case, confirmar_cadastro_use_case, login_use_case):
        self.criar_usuario_use_case = criar_usuario_use_case
        self.listar_usuarios_use_case = listar_usuarios_use_case
        self.confirmar_cadastro_use_case = confirmar_cadastro_use_case
        self.login_use_case = login_use_case
    
    def criar_usuario(self):
        data = request.get_json()
        try:
            usuario = self.criar_usuario_use_case.execute(
                nome=data.get('nome'),
                cnpj=data.get('cnpj'),
                email=data.get('email'),
                celular=data.get('celular'),
                senha=data.get('senha')
            )
            return jsonify({
                'mensagem': 'Usuário salvo, mas aguardando verificação de SMS.',
                'id_usuario': usuario.id
            }), 201
        except ValueError as e:
            return jsonify({'erro': str(e)}), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return jsonify({'erro': 'Erro ao cadastrar usuário', 'detalhes': str(e)}), 500
    @jwt_required()
    def listar_usuario(self):
        usuarios = self.listar_usuarios_use_case.execute()
        return jsonify([{
            'id': u.id,
            'nome': u.nome,
            'cnpj': u.cnpj,
            'email': u.email,
            'celular': u.celular,
            'status': u.status
        } for u in usuarios])
    
    def confirmar_cadastro(self, id):
        data = request.get_json()
        codigo = data.get('codigo_otp')
        
        try:
            verificado = self.confirmar_cadastro_use_case.execute(id, codigo)
            if verificado:
                return jsonify({'mensagem': 'Conta ativada com sucesso!'}), 200
            return jsonify({'erro': 'Código inválido'}), 400
        except ValueError as e:
            return jsonify({'erro': str(e)}), 404
        
    def login(self):
        dados = request.get_json()
        try:
            token = self.login_use_case.execute(dados.get('email'), dados.get('senha'))
            return jsonify({"access_token": token}), 200
            
        except ValueError as e:
            return jsonify({"erro": str(e)}), 401
        except Exception as e:
            return jsonify({"erro": "Erro interno no servidor"}), 500
