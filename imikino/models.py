# Aqui é onde irão ficar minhas tabelas do banco de dados
from imikino import database, login_manager
from flask_login import UserMixin  # é um parametro que vai passar para a nossa classe para ele entender quem é o usuário ativo


@login_manager.user_loader
def load_usuario(id_usuario):  # vai encontrar um usuario pelo id do usuario
    return Usuario.query.get(int(id_usuario))


# Tabela usuário
class Usuario(database.Model, UserMixin):
    # colunas do banco de dados
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)  # nullable=False -> É obrigatório | unique=True -> Tem que ser único
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    jogo_favorito = database.Column(database.String, default='Não Informado')
    avaliacoes = database.relationship('Avaliacao', backref='autor', lazy=True)


class Jogos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    lancamento = database.Column(database.Integer, nullable=False)
    descricao = database.Column(database.String, nullable=False)
    genero = database.Column(database.String, nullable=False)
    desenvolvedor = database.Column(database.String, nullable=False)
    foto_jogo = database.Column(database.String, nullable=False)
    media_jogos = database.Column(database.String, nullable=True)
    avaliacoes = database.relationship('Avaliacao', backref='jogo', lazy=True)


class Avaliacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_jogos = database.Column(database.Integer, database.ForeignKey('jogos.id'), nullable=False)

    avaliacao = database.Column(database.Integer)