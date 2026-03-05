def configure_routes(app, usuario_controller, produto_controller):
    app.add_url_rule('/cadastra_usuario', view_func=usuario_controller.criar_usuario, methods=['POST'])
    app.add_url_rule('/confirma_cadastro/<int:id>', view_func=usuario_controller.confirmar_cadastro, methods=['POST'])
    app.add_url_rule('/listar_usuario', view_func=usuario_controller.listar_usuario, methods=['GET'])
    app.add_url_rule('/login', view_func=usuario_controller.login, methods=['POST'])
    
    app.add_url_rule('/cadastra_produto', view_func=produto_controller.criar_produto, methods=['POST'])
    app.add_url_rule('/listar_produto', view_func=produto_controller.listar_produtos, methods=['GET'])
    app.add_url_rule('/listar_produto/<int:id>', view_func=produto_controller.listar_produtos, methods=['GET'])
