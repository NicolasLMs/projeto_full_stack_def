from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

class VendaController:
    def __init__(self, registrar_venda_use_case, historico_vendas_use_case):
        self.registrar_venda_use_case = registrar_venda_use_case
        self.historico_vendas_use_case = historico_vendas_use_case

    @jwt_required()
    def registrar_venda(self):
        data = request.get_json()
        id_usuario = int(get_jwt_identity())

        id_produto = data.get('id_produto')
        quantidade_vendida = data.get('quantidade_vendida')

        # Validação de campos obrigatórios
        if id_produto is None:
            return jsonify({'erro': 'Campo id_produto é obrigatório'}), 400
        if quantidade_vendida is None:
            return jsonify({'erro': 'Campo quantidade_vendida é obrigatório'}), 400
        if not isinstance(id_produto, int) or id_produto <= 0:
            return jsonify({'erro': 'id_produto deve ser um inteiro positivo'}), 400
        if not isinstance(quantidade_vendida, int) or quantidade_vendida <= 0:
            return jsonify({'erro': 'quantidade_vendida deve ser um inteiro positivo'}), 400

        try:
            venda = self.registrar_venda_use_case.execute(
                id_produto=id_produto,
                quantidade_vendida=quantidade_vendida,
                id_usuario=id_usuario
            )
            return jsonify({
                'id': venda.id,
                'id_produto': venda.id_produto,
                'quantidade_vendida': venda.quantidade_vendida,
                'preco_unitario': venda.preco_unitario
            }), 201
        except PermissionError as e:
            return jsonify({'erro': str(e)}), 403
        except LookupError as e:
            return jsonify({'erro': str(e)}), 404
        except ValueError as e:
            return jsonify({'erro': str(e)}), 422
        except Exception as e:
            return jsonify({'erro': 'Erro ao registrar venda', 'detalhes': str(e)}), 500

    @jwt_required()
    def historico_vendas(self):
        id_usuario = int(get_jwt_identity())
        vendas = self.historico_vendas_use_case.execute(id_usuario)
        return jsonify([{
            'id': v.id,
            'id_produto': v.id_produto,
            'quantidade_vendida': v.quantidade_vendida,
            'preco_unitario': v.preco_unitario
        } for v in vendas]), 200
