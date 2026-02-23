from  service.usuario_service import usuario_controller

def usuario(app):
    app.add_url_rule('/cadastra_usuario', view_func=usuario_controller.criar_usuario, methods = ['POST'])
    app.add_url_rule('/confirma_cadastro/<int:id>', view_func=usuario_controller.confirmar_cadastro, methods = ['POST'])

    
    app.add_url_rule('/listar_usuario', view_func=usuario_controller.listar_usuario, methods = ['GET'])
    

