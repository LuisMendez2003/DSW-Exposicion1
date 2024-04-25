import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from model.predio import Predio 
from utils import db
from config import DATABASE_CONNECTION

basedir = os.path.abspath(os.path.dirname(__file__))

#Inicializa la apliación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

bootstrap = Bootstrap(app)
moment = Moment(app)

#Se realiza el formulario
class NameForm(FlaskForm):
    name = StringField('Ingrese el Predio ID:', validators=[DataRequired()])
     
    submit = SubmitField('Enviar')

#Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        id_predio = int(form.name.data)
        predio = Predio.query.get(id_predio)
        if predio is None:
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'),
                           known = session.get('known', False))


from utils.db import init_app
init_app(app)

if(__name__) == '__main__':
    app.run(debug = True)