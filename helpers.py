import os
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField,PasswordField
from jogoteca import app


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.data_required(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Adicionar')

class FormularioUsuario(FlaskForm):
    nickname=StringField('Nickname',[validators.data_required(), validators.Length(min=1, max=8)])
    senha=PasswordField('Senha',[validators.data_required(), validators.Length(min=1, max=100)])
    login= SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa padrao.svg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa padrao.svg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
