from flask import render_template, request, redirect, session, flash, url_for,send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo,FormularioJogo
import time


@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    lista = Jogos.query.order_by(Jogos.id)
    lista_imagens = []
    for capa in lista:
        lista_imagens.append(recupera_imagem(capa.id))
    return render_template("lista.html", titulo='Jogos', jogos=lista,capas=lista_imagens)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', id=id, titulo='Editando o Jogo', capa_jogo=capa_jogo,form=form)


@app.route('/criar', methods=['POST', ])
def criar():

    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        flash("Formulário não é Valido")
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome,categoria=categoria,console=console)

    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'uploads/capa{novo_jogo.id}-{timestamp}.jpg')

    novo_jogo.capa = f'uploads/capa{novo_jogo.id}-{timestamp}.jpg'
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    deleta_arquivo(jogo.id)
    timestamp = time.time()
    arquivo.save(f'uploads/capa{jogo.id}-{timestamp}.jpg')

    jogo.capa = f'uploads/capa{jogo.id}-{timestamp}.jpg'

    db.session.add(jogo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar')))

    jogo = Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

