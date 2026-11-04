from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps

from app.categorias import categorias
from app.extensions import db
from app.models import Categoria


def administrador(f):

    @wraps(f)
    def decorador(*args, **kwargs):

        if current_user.rol != 'admin':
            abort(403)

        return f(*args, **kwargs)

    return decorador


@categorias.route('/')
@login_required
@administrador
def listar():

    lista = Categoria.query.all()

    return render_template('categorias/listar.html', categorias=lista)


@categorias.route('/crear', methods=['GET', 'POST'])
@login_required
@administrador
def crear():

    if request.method == 'POST':

        nombre = request.form['nombre']

        descripcion = request.form['descripcion']

        existente = Categoria.query.filter_by(nombre=nombre).first()

        if existente:

            flash('La categoría ya existe.', 'danger')

            return redirect(url_for('categorias.crear'))

        nueva = Categoria(
            nombre=nombre,
            descripcion=descripcion
        )

        db.session.add(nueva)

        db.session.commit()

        flash('Categoría registrada correctamente.', 'success')

        return redirect(url_for('categorias.listar'))

    return render_template('categorias/crear.html')


@categorias.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@administrador
def editar(id):

    categoria = db.session.get(Categoria, id)

    if categoria is None:
        abort(404)

    if request.method == 'POST':

        nombre = request.form['nombre']

        descripcion = request.form['descripcion']

        existente = Categoria.query.filter(
            Categoria.nombre == nombre,
            Categoria.id != id
        ).first()

        if existente:

            flash('Ya existe otra categoría con ese nombre.', 'danger')

            return redirect(url_for('categorias.editar', id=id))

        categoria.nombre = nombre

        categoria.descripcion = descripcion

        db.session.commit()

        flash('Categoría modificada correctamente.', 'success')

        return redirect(url_for('categorias.listar'))

    return render_template('categorias/editar.html', categoria=categoria)


@categorias.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@administrador
def eliminar(id):

    categoria = db.session.get(Categoria, id)

    if categoria is None:
        abort(404)

    if categoria.anuncios:

        flash('No puedes eliminar una categoría que tiene anuncios registrados.', 'warning')

        return redirect(url_for('categorias.listar'))

    db.session.delete(categoria)

    db.session.commit()

    flash('Categoría eliminada correctamente.', 'success')

    return redirect(url_for('categorias.listar'))