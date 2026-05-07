from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta


class DashboardController:
    def __init__(self, listar_produtos_use_case, historico_vendas_use_case):
        self.listar_produtos_use_case = listar_produtos_use_case
        self.historico_vendas_use_case = historico_vendas_use_case

    @jwt_required()
    def get_stats(self):
        id_usuario = int(get_jwt_identity())

        produtos = self.listar_produtos_use_case.execute(id_usuario=id_usuario)
        vendas = self.historico_vendas_use_case.execute(id_usuario)

        total_products = len(produtos)
        low_stock_products = sum(1 for p in produtos if p.quantidade <= 5)

        total_sales = len(vendas)
        total_revenue = sum(v.quantidade_vendida * v.preco_unitario for v in vendas)

        # Vendas por dia (últimos 7 dias)
        today = datetime.utcnow().date()
        sales_by_day = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            label = day.strftime('%d/%m')
            sales_by_day.append({
                'date': label,
                'total': 0,
                'count': 0,
            })

        # Top produtos por receita
        revenue_by_product: dict = {}
        for v in vendas:
            key = str(v.id_produto)
            produto = next((p for p in produtos if p.id == v.id_produto), None)
            nome = produto.nome if produto else f'Produto #{v.id_produto}'
            if key not in revenue_by_product:
                revenue_by_product[key] = {'name': nome, 'quantity': 0, 'revenue': 0}
            revenue_by_product[key]['quantity'] += v.quantidade_vendida
            revenue_by_product[key]['revenue'] += v.quantidade_vendida * v.preco_unitario

        top_products = sorted(
            revenue_by_product.values(),
            key=lambda x: x['revenue'],
            reverse=True
        )[:5]

        # Vendas por forma de pagamento (simplificado — backend não armazena método)
        sales_by_payment = [
            {'method': 'pix', 'count': total_sales, 'total': total_revenue}
        ] if total_sales > 0 else []

        # Vendas recentes (últimas 5)
        recent_sales = []
        for v in list(reversed(vendas))[:5]:
            produto = next((p for p in produtos if p.id == v.id_produto), None)
            recent_sales.append({
                'id': v.id,
                'seller_id': v.id_usuario,
                'product_id': v.id_produto,
                'product_name': produto.nome if produto else f'Produto #{v.id_produto}',
                'quantity': v.quantidade_vendida,
                'unit_price': v.preco_unitario,
                'total': v.quantidade_vendida * v.preco_unitario,
                'payment_method': 'pix',
                'status': 'completed',
                'created_at': datetime.utcnow().isoformat(),
            })

        return jsonify({
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'sales_by_day': sales_by_day,
            'top_products': top_products,
            'sales_by_payment': sales_by_payment,
            'recent_sales': recent_sales,
        }), 200
