from domain.ports.usuario_repository import UsuarioRepository
from domain.entities.usuario import Usuario
from infrastructure.database.models import db, UsuarioModel

class UsuarioRepositoryImpl(UsuarioRepository):
    def criar(self, usuario):
        from sqlalchemy.exc import IntegrityError
        try:
            usuario_model = UsuarioModel(
                nome=usuario.nome,
                cnpj=usuario.cnpj,
                email=usuario.email,
                celular=usuario.celular,
                senha=usuario.senha,
                status=usuario.status
            )
            db.session.add(usuario_model)
            db.session.commit()
            usuario.id = usuario_model.id
            return usuario
        except IntegrityError as e:
            db.session.rollback()
            if 'usuario.email' in str(e):
                raise ValueError('Email já cadastrado')
            elif 'usuario.cnpj' in str(e):
                raise ValueError('CNPJ já cadastrado')
            raise ValueError('Erro ao cadastrar usuário')
    
    def listar_todos(self):
        usuarios_model = UsuarioModel.query.all()
        return [Usuario(
            nome=u.nome,
            cnpj=u.cnpj,
            email=u.email,
            celular=u.celular,
            senha=u.senha,
            id=u.id,
            status=u.status
        ) for u in usuarios_model]
    
    def buscar_por_email(self, email):
        usuario_model = UsuarioModel.query.filter_by(email=email).first()
        if not usuario_model:
            return None
        return Usuario(
            nome=usuario_model.nome,
            cnpj=usuario_model.cnpj,
            email=usuario_model.email,
            celular=usuario_model.celular,
            senha=usuario_model.senha,
            id=usuario_model.id,
            status=usuario_model.status
        )
    
    def atualizar(self, usuario):
        usuario_model = UsuarioModel.query.get(usuario.id)
        if usuario_model:
            usuario_model.nome = usuario.nome
            usuario_model.cnpj = usuario.cnpj
            usuario_model.email = usuario.email
            usuario_model.celular = usuario.celular
            usuario_model.senha = usuario.senha
            usuario_model.status = usuario.status
            db.session.commit()
        return usuario

            