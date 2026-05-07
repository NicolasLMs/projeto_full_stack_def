from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

from infrastructure.database.models import db
from infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl
from infrastructure.repositories.produto_repository_impl import ProdutoRepositoryImpl
from infrastructure.services.twilio_sms_service import TwilioSmsService
from infrastructure.services.hash_service import HashServiceImpl
from infrastructure.services.token_service import JWTService

from application.use_cases.criar_usuario import CriarUsuarioUseCase
from application.use_cases.listar_usuarios import ListarUsuariosUseCase
from application.use_cases.confirmar_cadastro_usuario import ConfirmarCadastroUsuarioUseCase
from application.use_cases.login_usuario import LoginUseCase
from application.use_cases.buscar_por_email import Buscar_por_EmailUsuarioUseCase
from application.use_cases.atualizar_cadastro import AtualizarCadastroUsuarioUseCase
from application.use_cases.criar_produto import CriarProdutoUseCase
from application.use_cases.listar_produtos import ListarProdutosUseCase
from application.use_cases.atualizar_produto import AtualizarProdutoUseCase
from application.use_cases.registrar_venda import RegistrarVendaUseCase
from application.use_cases.historico_vendas import HistoricoVendasUseCase

from adapters.http.usuario_controller import UsuarioController
from adapters.http.produto_controller import ProdutoController
from adapters.http.venda_controller import VendaController
from adapters.http.dashboard_controller import DashboardController
from adapters.http.routes import configure_routes

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

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
hash_service = HashServiceImpl()
token_service = JWTService()

from infrastructure.repositories.venda_repository_impl import VendaRepositoryImpl
venda_repository = VendaRepositoryImpl()

# Casos de uso
criar_usuario_use_case = CriarUsuarioUseCase(usuario_repository, sms_service, hash_service)
listar_usuarios_use_case = ListarUsuariosUseCase(usuario_repository)
confirmar_cadastro_use_case = ConfirmarCadastroUsuarioUseCase(usuario_repository, sms_service)
login_use_case = LoginUseCase(usuario_repository, hash_service, token_service)
buscar_usuario_use_case= Buscar_por_EmailUsuarioUseCase(usuario_repository)
atualizar_cadastro_use_case = AtualizarCadastroUsuarioUseCase(usuario_repository, hash_service)
criar_produto_use_case = CriarProdutoUseCase(produto_repository)
listar_produtos_use_case = ListarProdutosUseCase(produto_repository)
atualizar_produto_use_case = AtualizarProdutoUseCase(produto_repository)
registrar_venda_use_case = RegistrarVendaUseCase(venda_repository, produto_repository, usuario_repository)
historico_vendas_use_case = HistoricoVendasUseCase(venda_repository)
# Controllers
usuario_controller = UsuarioController(criar_usuario_use_case, listar_usuarios_use_case, confirmar_cadastro_use_case, login_use_case, buscar_usuario_use_case, atualizar_cadastro_use_case)
produto_controller = ProdutoController(criar_produto_use_case, listar_produtos_use_case, atualizar_produto_use_case)
venda_controller = VendaController(registrar_venda_use_case, historico_vendas_use_case)
dashboard_controller = DashboardController(listar_produtos_use_case, historico_vendas_use_case)

# Rotas
configure_routes(app, usuario_controller, produto_controller, venda_controller, dashboard_controller)

if __name__ == '__main__':
    app.run(debug=True)
