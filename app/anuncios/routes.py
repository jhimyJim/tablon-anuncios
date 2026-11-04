from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime

from app.anuncios import anuncios
from app.extensions import db
from app.models import Anuncio, Categoria


def administrador(f):

    @wraps(f)
    def decorador(*args, **kwargs):

        if current_user.rol != 'admin':
            abort(403)

        return f(*args, **kwargs)

    return decorador


@anuncios.route('/')
@login_required
@administrador
def listar():

    lista = Anuncio.query.order_by(Anuncio.id.desc()).all()

    return render_template('anuncios/listar.html', anuncios=lista)


@anuncios.route('/crear', methods=['GET', 'POST'])
@login_required
@administrador
def crear():

    lista = Categoria.query.all()

    if not lista:

        flash('Primero debes registrar una categoría.', 'warning')

        return redirect(url_for('categorias.crear'))

    if request.method == 'POST':

        titulo = request.form['titulo']

        contenido = request.form['contenido']

        id_categoria = request.form['id_categoria']

        nuevo = Anuncio(
            titulo=titulo,
            contenido=contenido,
            fecha_publicacion=datetime.utcnow(),
            estado='publicado',
            id_usuario=current_user.id,
            id_categoria=id_categoria
        )

        db.session.add(nuevo)

        db.session.commit()

        flash('Anuncio publicado correctamente.', 'success')

        return redirect(url_for('anuncios.listar'))

    return render_template('anuncios/crear.html', categorias=lista)


@anuncios.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@administrador
def editar(id):

    anuncio = db.session.get(Anuncio, id)

    if anuncio is None:
        abort(404)

    lista = Categoria.query.all()

    if request.method == 'POST':

        anuncio.titulo = request.form['titulo']

        anuncio.contenido = request.form['contenido']

        anuncio.id_categoria = request.form['id_categoria']

        anuncio.estado = request.form['estado']

        db.session.commit()

        flash('Anuncio modificado correctamente.', 'success')

        return redirect(url_for('anuncios.listar'))

    return render_template(
        'anuncios/editar.html',
        anuncio=anuncio,
        categorias=lista
    )


@anuncios.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@administrador
def eliminar(id):

    anuncio = db.session.get(Anuncio, id)

    if anuncio is None:
        abort(404)

    db.session.delete(anuncio)

    db.session.commit()

    flash('Anuncio eliminado correctamente.', 'success')

    return redirect(url_for('anuncios.listar'))