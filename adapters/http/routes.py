def configure_routes(app, usuario_controller, produto_controller, venda_controller, dashboard_controller):
    # ── Auth / Usuários ──────────────────────────────────────────────────────
    app.add_url_rule('/api/auth/login', view_func=usuario_controller.login, methods=['POST'])
    app.add_url_rule('/api/sellers/register', view_func=usuario_controller.criar_usuario, methods=['POST'])
    app.add_url_rule('/api/sellers/send-activation', view_func=usuario_controller.send_activation, methods=['POST'])
    app.add_url_rule('/api/sellers/activate', view_func=usuario_controller.confirmar_cadastro_por_codigo, methods=['POST'])

    # Rotas legadas (mantidas para compatibilidade)
    app.add_url_rule('/cadastra_usuario', view_func=usuario_controller.criar_usuario, methods=['POST'], endpoint='cadastra_usuario_legacy')
    app.add_url_rule('/confirma_cadastro/<string:email>', view_func=usuario_controller.confirmar_cadastro, methods=['POST'])
    app.add_url_rule('/listar_usuario', view_func=usuario_controller.listar_usuario, methods=['GET'])
    app.add_url_rule('/login', view_func=usuario_controller.login_legacy, methods=['POST'])
    app.add_url_rule('/atualizar_usuario/<string:email>', view_func=usuario_controller.atualizar_usuario, methods=['PUT'])
    app.add_url_rule('/buscar_por_email_usuario/<string:email>', view_func=usuario_controller.buscar_por_email_usuario, methods=['GET'])

    # ── Produtos ─────────────────────────────────────────────────────────────
    app.add_url_rule('/api/products', view_func=produto_controller.criar_produto, methods=['POST'])
    app.add_url_rule('/api/products', view_func=produto_controller.listar_produtos, methods=['GET'], endpoint='api_listar_produtos')
    app.add_url_rule('/api/products/<int:id>', view_func=produto_controller.listar_produto_por_id, methods=['GET'])
    app.add_url_rule('/api/products/<int:id>', view_func=produto_controller.atualizar_produto, methods=['PUT'], endpoint='api_atualizar_produto')
    app.add_url_rule('/api/products/<int:id>', view_func=produto_controller.deletar_produto, methods=['DELETE'])

    # Rotas legadas
    app.add_url_rule('/cadastra_produto', view_func=produto_controller.criar_produto, methods=['POST'], endpoint='cadastra_produto_legacy')
    app.add_url_rule('/listar_produto', view_func=produto_controller.listar_produtos, methods=['GET'], endpoint='listar_produto_legacy')
    app.add_url_rule('/listar_produto/<int:id>', view_func=produto_controller.listar_produto_por_id, methods=['GET'], endpoint='listar_produto_por_id_legacy')
    app.add_url_rule('/atualizar_produto/<int:id>', view_func=produto_controller.atualizar_produto, methods=['PUT'], endpoint='atualizar_produto_legacy')

    # ── Vendas ────────────────────────────────────────────────────────────────
    app.add_url_rule('/api/sales', view_func=venda_controller.registrar_venda, methods=['POST'])
    app.add_url_rule('/api/sales', view_func=venda_controller.historico_vendas, methods=['GET'], endpoint='api_historico_vendas')
    app.add_url_rule('/api/sales/<int:id>', view_func=venda_controller.deletar_venda, methods=['DELETE'])

    # Rotas legadas
    app.add_url_rule('/registrar_venda', view_func=venda_controller.registrar_venda, methods=['POST'], endpoint='registrar_venda_legacy')
    app.add_url_rule('/historico_vendas', view_func=venda_controller.historico_vendas, methods=['GET'], endpoint='historico_vendas_legacy')

    # ── Dashboard ─────────────────────────────────────────────────────────────
    app.add_url_rule('/api/dashboard/stats', view_func=dashboard_controller.get_stats, methods=['GET'])
