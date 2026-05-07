from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


class UsuarioController:
    def __init__(self, criar_usuario_use_case, listar_usuarios_use_case,
                 confirmar_cadastro_use_case, login_use_case,
                 buscar_usuario_por_email_use_case, atualizar_cadastro_use_case):
        self.criar_usuario_use_case = criar_usuario_use_case
        self.listar_usuarios_use_case = listar_usuarios_use_case
        self.confirmar_cadastro_use_case = confirmar_cadastro_use_case
        self.login_use_case = login_use_case
        self.buscar_usuario_por_email_use_case = buscar_usuario_por_email_use_case
        self.atualizar_cadastro_use_case = atualizar_cadastro_use_case

    # ── POST /api/sellers/register ────────────────────────────────────────────
    def criar_usuario(self):
        data = request.get_json()
        try:
            usuario = self.criar_usuario_use_case.execute(
                nome=data.get('name') or data.get('nome'),
                cnpj=data.get('cnpj', ''),
                email=data.get('email'),
                celular=data.get('whatsapp') or data.get('phone') or data.get('celular'),
                senha=data.get('password') or data.get('senha')
            )
            return jsonify({
                'message': 'Cadastro realizado com sucesso',
                'email': usuario.email
            }), 201
        except ValueError as e:
            return jsonify({'message': str(e)}), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return jsonify({'message': 'Erro ao cadastrar usuário', 'details': str(e)}), 500

    # ── POST /api/sellers/send-activation ────────────────────────────────────
    def send_activation(self):
        """Reenvia o código OTP para o celular informado."""
        data = request.get_json()
        phone = data.get('phone') or data.get('celular')
        if not phone:
            return jsonify({'message': 'Número de telefone é obrigatório'}), 400
        # O código já foi enviado no cadastro; aqui apenas confirmamos
        return jsonify({'message': 'Código enviado'}), 200

    # ── POST /api/sellers/activate ────────────────────────────────────────────
    def confirmar_cadastro_por_codigo(self):
        """Ativa a conta usando email + código OTP."""
        data = request.get_json()
        email = data.get('email')
        codigo = data.get('code') or data.get('codigo_otp')

        if not email or not codigo:
            return jsonify({'message': 'Email e código são obrigatórios'}), 400

        try:
            verificado = self.confirmar_cadastro_use_case.execute(email, codigo)
            if verificado:
                return jsonify({'message': 'Conta ativada com sucesso'}), 200
            return jsonify({'message': 'Código inválido'}), 400
        except ValueError as e:
            return jsonify({'message': str(e)}), 404

    # ── POST /api/auth/login ──────────────────────────────────────────────────
    def login(self):
        dados = request.get_json()
        try:
            token = self.login_use_case.execute(
                dados.get('email'),
                dados.get('password') or dados.get('senha')
            )
            # Busca dados do usuário para retornar junto com o token
            usuario = self.buscar_usuario_por_email_use_case.execute(dados.get('email'))
            return jsonify({
                'token': token,
                'user': {
                    'id': usuario.id,
                    'name': usuario.nome,
                    'email': usuario.email,
                    'role': 'seller',
                    'seller_id': usuario.id
                }
            }), 200
        except ValueError as e:
            return jsonify({'message': str(e)}), 401
        except Exception as e:
            return jsonify({'message': 'Erro interno no servidor'}), 500

    # ── POST /login (legado) ──────────────────────────────────────────────────
    def login_legacy(self):
        dados = request.get_json()
        try:
            token = self.login_use_case.execute(dados.get('email'), dados.get('senha'))
            return jsonify({'access_token': token}), 200
        except ValueError as e:
            return jsonify({'erro': str(e)}), 401
        except Exception as e:
            return jsonify({'erro': 'Erro interno no servidor'}), 500

    # ── GET /listar_usuario ───────────────────────────────────────────────────
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

    # ── POST /confirma_cadastro/<email> (legado) ──────────────────────────────
    def confirmar_cadastro(self, email):
        data = request.get_json()
        codigo = data.get('codigo_otp')
        try:
            verificado = self.confirmar_cadastro_use_case.execute(email, codigo)
            if verificado:
                return jsonify({'mensagem': 'Conta ativada com sucesso!'}), 200
            return jsonify({'erro': 'Código inválido'}), 400
        except ValueError as e:
            return jsonify({'erro': str(e)}), 404

    # ── PUT /atualizar_usuario/<email> ────────────────────────────────────────
    @jwt_required()
    def atualizar_usuario(self, email):
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

    # ── GET /buscar_por_email_usuario/<email> ─────────────────────────────────
    @jwt_required()
    def buscar_por_email_usuario(self, email):
        try:
            usuario = self.buscar_usuario_por_email_use_case.execute(email)
            return jsonify({
                'id': usuario.id,
                'nome': usuario.nome,
                'telefone': usuario.celular,
                'email': usuario.email,
                'status': usuario.status
            }), 200
        except ValueError as e:
            return jsonify({'erro': str(e)}), 404
        except Exception as e:
            return jsonify({'erro': 'Erro ao tentar encontrar usuário', 'detalhes': str(e)}), 500
