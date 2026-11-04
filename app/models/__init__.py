from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class Usuario(UserMixin, db.Model):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    correo = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    rol = db.Column(db.String(20), default='usuario')

    anuncios = db.relationship('Anuncio', back_populates='usuario')

    def verificar_password(self, password):

        from werkzeug.security import check_password_hash

        return check_password_hash(self.password, password)
class Categoria(db.Model):

    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), unique=True, nullable=False)

    descripcion = db.Column(db.String(255))

    anuncios = db.relationship('Anuncio', back_populates='categoria')


class Anuncio(db.Model):

    __tablename__ = 'anuncios'

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(150), nullable=False)

    contenido = db.Column(db.Text, nullable=False)

    fecha_publicacion = db.Column(db.DateTime, default=datetime.utcnow)

    estado = db.Column(db.String(20), default='publicado')

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='anuncios')

    categoria = db.relationship('Categoria', back_populates='anuncios')