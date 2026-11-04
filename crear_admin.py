from app import create_app
from app.extensions import db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():

    usuario = Usuario.query.filter_by(correo='admin@anuncios.com').first()

    if usuario:

        print('El administrador ya existe.')

    else:

        admin = Usuario(
            nombre='Administrador',
            correo='admin@anuncios.com',
            password=generate_password_hash('Admin123*'),
            rol='admin'
        )

        db.session.add(admin)

        db.session.commit()

        print('Administrador creado correctamente.')