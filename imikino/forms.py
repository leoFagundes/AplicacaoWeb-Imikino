from flask_wtf import FlaskForm  # classe pronta do Flask para criação de formulários
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField # wtforms vem junto com o flask_wtf -> estamos importando o que vamos colocar nos campos abaixo
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  # VALIDADORES ... DataRequired -> Campo Obrigatório | Length -> Tamanho mínimo de um campo | Email -> Verificar se é um email válido | EqualTo -> Verificar se um campo é igual ao outro (no caso o de senha)
from imikino.models import Usuario
from flask_login import current_user



class FormCriarConta(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='E-mail inválido, preencha um e-mail válido para continuar')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais')])
    botao_submit_criarconta = SubmitField('Criar Conta')


    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError("Esse nickname já foi cadastrado. Tente usar outro nick para continuar")


    def validate_email(self, email):  # obrigatoriamente tem que ser validate_ o inicio da sua função pq o validate_on_submite ele toda automaticamente todas as funções que começam  com valite_ -> Essa função faz com que valide se não tem emails repetidos no banco de dados
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Esse E-mail já foi cadastrado. Tente usar outro e-mail para continuar")


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    jogo_favorito = SelectField('Jogo Favorito', coerce=str, choices=['Não informado', 'Cuphead', 'Diablo III', 'Fortnite', 'League of Legends', 'Overwatch', 'Stardew Valley', 'Counter-Strike: GO', 'World of Warcraft', 'The Witcher 3', 'Minecraft', 'Cities: Skylines', 'Child of Light', 'Doki Doki Literature Club!', 'Persona 5', 'Grand Theft Auto V', 'The Legend of Zelda'])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')


    def validate_username(self, username):
        #verificar se ele mudou de nome
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError("Já existe um usuário com esse Nickname")


    def validate_email(self, email):  
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("Já existe um usuário com esse e-mail")


class Avaliacoes(FlaskForm):
    avaliacao = SelectField('★', coerce=int, choices=[0, 1, 2, 3, 4, 5])
    botao_submit_avaliar = SubmitField('Salvar')


class IdSteam(FlaskForm):
    id_steam = StringField('Id Steam')
    botao_submit_pesquisar = SubmitField('Pesquisar')