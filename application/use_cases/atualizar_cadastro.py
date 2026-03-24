class AtualizarCadastroUsuarioUseCase:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository
    
    def execute(self, email, nome=None, cnpj=None, celular=None, senha=None):
        usuario = self.usuario_repository.buscar_por_email(email)
        if not usuario:
            raise ValueError('Usuário não encontrado')
        
        if nome is not None:
            usuario.nome = nome
        if cnpj is not None:
            usuario.cnpj = cnpj
        if celular is not None:
            usuario.celular = celular
        if senha is not None:
            usuario.senha = senha
        
        self.usuario_repository.atualizar(usuario)
        return usuario
