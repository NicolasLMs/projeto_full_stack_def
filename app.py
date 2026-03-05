from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from infrastructure.database.models import db
from infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from infrastructure.repositories.produto_repository_impl import ProdutoRepositoryImpl
from infrastructure.services.twilio_sms_service import TwilioSmsService

from application.use_cases.criar_usuario import CriarUsuarioUseCase
from application.use_cases.listar_usuarios import ListarUsuariosUseCase
from application.use_cases.confirmar_cadastro_usuario import ConfirmarCadastroUsuarioUseCase
from application.use_cases.login_usuario import LoginUseCase
from application.use_cases.criar_produto import CriarProdutoUseCase
from application.use_cases.listar_produtos import ListarProdutosUseCase

from adapters.http.usuario_controller import UsuarioController
from adapters.http.produto_controller import ProdutoController
from adapters.http.routes import configure_routes

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'meu_banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

# Infraestrutura
usuario_repository = UsuarioRepositoryImpl()
produto_repository = ProdutoRepositoryImpl()
sms_service = TwilioSmsService()

# Casos de uso
criar_usuario_use_case = CriarUsuarioUseCase(usuario_repository, sms_service)
listar_usuarios_use_case = ListarUsuariosUseCase(usuario_repository)
confirmar_cadastro_use_case = ConfirmarCadastroUsuarioUseCase(usuario_repository, sms_service)
login_use_case = LoginUseCase(usuario_repository)
criar_produto_use_case = CriarProdutoUseCase(produto_repository)
listar_produtos_use_case = ListarProdutosUseCase(produto_repository)

# Controllers
usuario_controller = UsuarioController(criar_usuario_use_case, listar_usuarios_use_case, confirmar_cadastro_use_case, login_use_case)
produto_controller = ProdutoController(criar_produto_use_case, listar_produtos_use_case)

# Rotas
configure_routes(app, usuario_controller, produto_controller)

if __name__ == '__main__':
    app.run(debug=True)
