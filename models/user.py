from database import db
from flask_login import UserMixin #herdar dessa biblioteca p n fazer na mao

class User(db.Model, UserMixin):
    #id (int), username(text), password(text)
    id = db.Column(db.Integer, primary_key=True) #criando variavel unica do tipo inteiro PRIMARY KEY (chave primária)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default='user')