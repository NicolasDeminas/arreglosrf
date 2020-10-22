import functools
from flask import Blueprint, flash, g, render_template, request, url_for, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .db import cnxn

bp = Blueprint('auth', __name__, url_prefix= '/auth')

@bp.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        db, c = cnxn()
        error = None
        c.execute('Select id from Usuarios where Usuario = ?', username)
        consulta=c.fetchone()
        if not username:
            error = 'Usuario requerido'
        if not password:
            error = 'Contraseña requerida'
        if consulta is not None:
            error = 'El usuario {} se encuentra registrado'.format(username)
        
        if error is None:
            c.execute('insert into usuarios (Usuario, Contraseña) values (?, ?)',(username, generate_password_hash(password)))
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        password = request.form["password"]
        db, c = cnxn()
        error = None
        c.execute('select * from Usuarios where Usuario = ?', username)
        usuario = c.fetchone()
        if usuario is None:
            error = "Usuario y/o contraseña invalida"
        elif not check_password_hash(usuario[2], password):
            error = "Usuario y/o contraseña invalida"
        
        if error is None:
            session.clear()
            session["user_id"] = usuario[0]
            return redirect(url_for("equipos.inicio"))
        
        flash(error)
    
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db, c = cnxn()
        c.execute('Select * from Usuarios where id = ?', user_id)
        g.user = c.fetchone()
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
