from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.auth import auth
from app.models import Usuario


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':

        correo = request.form['correo']

        password = request.form['password']

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.verificar_password(password):

            login_user(usuario)

            flash('Bienvenido al sistema.', 'success')

            return redirect(url_for('main.index'))

        flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():

    logout_user()

    flash('Sesión cerrada correctamente.', 'success')

    return redirect(url_for('auth.login'))