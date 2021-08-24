from logging import debug
import os 

from flask import Flask, app

def create_app():
    app= Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'MiLLave',
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    from . import db
    from . import auth
    from . import views
    from . import siembra
    from . import colgado
    from . import cosecha
    

    app.register_blueprint(colgado.bp)
    app.register_blueprint(cosecha.bp)
    app.register_blueprint(siembra.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    db.init_app(app)
    
    @app.route('/inicio')
    def inicio():
        return 'Hola'

    return app


