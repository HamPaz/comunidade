from flask import render_template, request, redirect, url_for, flash, abort
from comunidade import app, database, bcrypt
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade.models import Usuarios, Posts
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# lista_usuarios = ['Imperius', 'Locutus', 'Astarte', 'Diana']


@app.route('/')
def home():
    posts = Posts.query.order_by(Posts.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuarios.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuarios.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar.data)
            flash(f'{form_login.email.data} acessou a rede neural com sucesso.', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                if '/' in par_next:
                    par_next = par_next.replace('/', '')
                return redirect(url_for(par_next))
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha ao acessar rede neural. Email e/ou senha incorreto(s).', 'alert-danger')

    if form_criar.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar.senha.data)
        usuario = Usuarios(username=form_criar.username.data, email=form_criar.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Unidade borg {form_criar.username.data} assimilada em {form_login.email.data}.', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', formLogin=form_login, formCriar=form_criar)


@app.route('/sair')
@login_required
def sair():
    usuario_borg = current_user.username
    logout_user()
    flash(f'Borg {usuario_borg} desconectado da COMunidade com sucesso.', 'alert-primary')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto))
    return render_template('perfil.html', foto=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    if len(lista_cursos) > 0:
        return ';'.join(lista_cursos)
    else:
        return 'Não informado.'


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Dados atualizados com sucesso.', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto))
    return render_template('editarperfil.html', foto=foto_perfil, form=form)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Posts(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Relatório entregue com sucesso.', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Posts.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Relatório atualizado com sucesso.', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Posts.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Relatório eliminado com sucesso.', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)