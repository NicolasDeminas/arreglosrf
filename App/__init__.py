import os
from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="llave1",
        DATABASE_HOST = os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD = os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE")
    )

    from . import db

    db.init_app(app)

    from . import auth
    from . import equipos
    from . import arreglos
    app.register_blueprint(auth.bp)
    app.register_blueprint(equipos.bp)
    app.register_blueprint(arreglos.bp)

    @app.route("/base")
    def base():
        return render_template("base.html")

    return app