from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuarios.query.get(int(id_usuario))


class Usuarios(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto = database.Column(database.String, nullable=False, default='default.jpg')
    cursos = database.Column(database.String, nullable=False, default='Não informado.')
    posts = database.relationship('Posts', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)

class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    # criacao = database.Column(database.DateTime, nullable=False, default=datetime.now(datetime.UTC))
    criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)
