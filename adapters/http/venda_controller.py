from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


class VendaController:
    def __init__(self, registrar_venda_use_case, historico_vendas_use_case,
                 deletar_venda_use_case=None):
        self.registrar_venda_use_case = registrar_venda_use_case
        self.historico_vendas_use_case = historico_vendas_use_case
        self.deletar_venda_use_case = deletar_venda_use_case

    # ── POST /api/sales ───────────────────────────────────────────────────────
    @jwt_required()
    def registrar_venda(self):
        data = request.get_json()
        id_usuario = int(get_jwt_identity())

        # Aceita tanto o formato do frontend (product_id/quantity) quanto o legado
        id_produto = data.get('product_id') or data.get('id_produto')
        quantidade_vendida = data.get('quantity') or data.get('quantidade_vendida')
        forma_pagamento = data.get('payment_method') or data.get('forma_pagamento') or 'pix'

        FORMAS_VALIDAS = {'cash', 'credit_card', 'debit_card', 'pix', 'transfer'}
        if forma_pagamento not in FORMAS_VALIDAS:
            return jsonify({'message': f'Forma de pagamento inválida. Use: {", ".join(FORMAS_VALIDAS)}'}), 400

        if id_produto is None:
            return jsonify({'message': 'Campo product_id é obrigatório'}), 400
        if quantidade_vendida is None:
            return jsonify({'message': 'Campo quantity é obrigatório'}), 400
        if not isinstance(id_produto, int) or id_produto <= 0:
            return jsonify({'message': 'product_id deve ser um inteiro positivo'}), 400
        if not isinstance(quantidade_vendida, int) or quantidade_vendida <= 0:
            return jsonify({'message': 'quantity deve ser um inteiro positivo'}), 400

        try:
            venda = self.registrar_venda_use_case.execute(
                id_produto=id_produto,
                quantidade_vendida=quantidade_vendida,
                id_usuario=id_usuario,
                forma_pagamento=forma_pagamento
            )
            return jsonify(self._serialize(venda)), 201
        except PermissionError as e:
            return jsonify({'message': str(e)}), 403
        except LookupError as e:
            return jsonify({'message': str(e)}), 404
        except ValueError as e:
            return jsonify({'message': str(e)}), 422
        except Exception as e:
            return jsonify({'message': 'Erro ao registrar venda', 'details': str(e)}), 500

    # ── GET /api/sales ────────────────────────────────────────────────────────
    @jwt_required()
    def historico_vendas(self):
        id_usuario = int(get_jwt_identity())
        search = request.args.get('search', '').lower()
        status_filter = request.args.get('status', '')

        vendas = self.historico_vendas_use_case.execute(id_usuario)

        result = []
        for v in vendas:
            s = self._serialize(v)
            if status_filter and s['status'] != status_filter:
                continue
            if search and search not in (s.get('product_name') or '').lower():
                continue
            result.append(s)

        return jsonify(result), 200

    # ── DELETE /api/sales/<id> ────────────────────────────────────────────────
    @jwt_required()
    def deletar_venda(self, id):
        if self.deletar_venda_use_case:
            try:
                self.deletar_venda_use_case.execute(id)
                return jsonify({'message': 'Venda excluída'}), 200
            except ValueError as e:
                return jsonify({'message': str(e)}), 404
            except Exception as e:
                return jsonify({'message': str(e)}), 500
        return jsonify({'message': 'Operação não suportada'}), 501

    def _serialize(self, v):
        return {
            'id': v.id,
            'seller_id': v.id_usuario if hasattr(v, 'id_usuario') else 0,
            'product_id': v.id_produto,
            'product_name': getattr(v, 'nome_produto', f'Produto #{v.id_produto}'),
            'quantity': v.quantidade_vendida,
            'unit_price': v.preco_unitario,
            'total': v.quantidade_vendida * v.preco_unitario,
            'payment_method': getattr(v, 'forma_pagamento', 'pix'),
            'status': getattr(v, 'status', 'completed'),
            'notes': getattr(v, 'notes', ''),
            'created_at': getattr(v, 'created_at', '') or '',
        }
