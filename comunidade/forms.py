from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuarios
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome do borg: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha de acesso: ', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirme sua senha: ', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Assimilar')

    def validate_email(self, email):
        usuario = Usuarios.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe um borg usando essa rota de acesso.')


class FormLogin(FlaskForm):
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha de acesso: ', validators=[DataRequired(), Length(6, 20)])
    lembrar = BooleanField('Lembrar de mim')
    botao_submit_login = SubmitField('Acessar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do borg: ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    curso_excel = BooleanField('Excel')
    curso_vba = BooleanField('VBA')
    curso_powerbi = BooleanField('Power BI')
    curso_python = BooleanField('Python')
    curso_ppt = BooleanField('Power Point')
    curso_sql = BooleanField('SQL')

    botao_submit_editar_perfil = SubmitField('Gravar alterações')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuarios.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um borg usando essa rota de acesso.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(3, 140)])
    corpo = TextAreaField('Escreva seu texto', validators=[DataRequired()])
    bt_postar = SubmitField('Postar')