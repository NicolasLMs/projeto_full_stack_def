from service.produtos_service import produto_controller

def produto(app):
    app.add_url_rule('/cadastra_produto', view_func=produto_controller.criar_produto, methods = ['POST'])
    
    app.add_url_rule('/listar_produto', view_func=produto_controller.listar_produtos, methods = ['GET'])

    app.add_url_rule('/listar_produto/<int:id>', view_func=produto_controller.listar_produtos, methods = ['GET'])
