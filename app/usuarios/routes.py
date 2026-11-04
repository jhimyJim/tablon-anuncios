from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from functools import wraps

from app.usuarios import usuarios
from app.extensions import db
from app.models import Usuario


def administrador(f):

    @wraps(f)
    def decorador(*args, **kwargs):

        if current_user.rol != 'admin':
            abort(403)

        return f(*args, **kwargs)

    return decorador


@usuarios.route('/')
@login_required
@administrador
def listar():

    lista = Usuario.query.all()

    return render_template('usuarios/listar.html', usuarios=lista)


@usuarios.route('/crear', methods=['GET', 'POST'])
@login_required
@administrador
def crear():

    if request.method == 'POST':

        nombre = request.form['nombre']

        correo = request.form['correo']

        password = request.form['password']

        rol = request.form['rol']

        existente = Usuario.query.filter_by(correo=correo).first()

        if existente:

            flash('El correo ya está registrado.', 'danger')

            return redirect(url_for('usuarios.crear'))

        nuevo = Usuario(
            nombre=nombre,
            correo=correo,
            password=generate_password_hash(password),
            rol=rol
        )

        db.session.add(nuevo)

        db.session.commit()

        flash('Usuario registrado correctamente.', 'success')

        return redirect(url_for('usuarios.listar'))

    return render_template('usuarios/crear.html')


@usuarios.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@administrador
def editar(id):

    usuario = db.session.get(Usuario, id)

    if usuario is None:
        abort(404)

    if request.method == 'POST':

        nombre = request.form['nombre']

        correo = request.form['correo']

        rol = request.form['rol']

        existente = Usuario.query.filter(
            Usuario.correo == correo,
            Usuario.id != id
        ).first()

        if existente:

            flash('El correo ya pertenece a otro usuario.', 'danger')

            return redirect(url_for('usuarios.editar', id=id))

        usuario.nombre = nombre

        usuario.correo = correo

        usuario.rol = rol

        password = request.form['password']

        if password:

            usuario.password = generate_password_hash(password)

        db.session.commit()

        flash('Usuario modificado correctamente.', 'success')

        return redirect(url_for('usuarios.listar'))

    return render_template('usuarios/editar.html', usuario=usuario)


@usuarios.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@administrador
def eliminar(id):

    usuario = db.session.get(Usuario, id)

    if usuario is None:
        abort(404)

    if usuario.id == current_user.id:

        flash('No puedes eliminar tu propia cuenta.', 'danger')

        return redirect(url_for('usuarios.listar'))

    if usuario.anuncios:

        flash('No puedes eliminar un usuario que tiene anuncios registrados.', 'warning')

        return redirect(url_for('usuarios.listar'))

    db.session.delete(usuario)

    db.session.commit()

    flash('Usuario eliminado correctamente.', 'success')

    return redirect(url_for('usuarios.listar'))