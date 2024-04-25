from flask_sqlalchemy import SQLAlchemy

#Crea una instancia de SQLAlchemy
db = SQLAlchemy()

#Inicializa la aplicacion con la instanca SQLAlchemy
def init_app(app):
    db.init_app(app)