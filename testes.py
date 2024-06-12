from main import app, database

with app.app_context():
    database.drop_all()
    database.create_all()

# with app.app_context():
#     usuario1 = Usuarios(username='Imperius', email='imperius@borg.com', senha='123456')
#     usuario2 = Usuarios(username='Crotalus', email='crotalus@borg.com', senha='123456')
#     usuario3 = Usuarios(username='Locutus', email='locutus@borg.com', senha='123456')
#
#     database.session.add(usuario1)
#     database.session.add(usuario2)
#     database.session.add(usuario3)
#
#     database.session.commit()

# with app.app_context():
#     borgs = Usuarios.query.all()
#     print(borgs)
#     primeiro_borg = Usuarios.query.first()
#     print(primeiro_borg.username)
#     print('*' * 30)
#     borg_pesq = Usuarios.query.filter_by(email='crotalus@borg.com').first()
#     print(borg_pesq)
#     print(borg_pesq.username)

# with app.app_context():
#     postagem1 = Posts(id_usuario=1, titulo='Estou vivo', corpo='Devidamente assimilado!!!')
#     postagem2 = Posts(id_usuario=1, titulo='Assimilando', corpo='Buscando novos humanos para assimilação.')
#     database.session.add(postagem1)
#     database.session.add(postagem2)
#     database.session.commit()

# with app.app_context():
#     postagens = Posts.query.all()
#     print(postagens)
#     primeiro_post = Posts.query.first()
#     print(primeiro_post.autor)
#     print(primeiro_post.criacao)
#     print(primeiro_post.autor.username)
