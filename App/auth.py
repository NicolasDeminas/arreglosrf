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
        password_confirm = request.form["password_confirm"]
        db, c = cnxn()
        error = None
        c.execute('Select id from Usuarios where Usuario = ?', username)
        consulta=c.fetchone()
        if not username:
            error = 'Usuario requerido'
        if not password:
            error = 'Contraseña requerida'
        if password == password_confirm:
            pass
        else:
            error = 'Verifique que las contraseñas sean iguales'
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
            return redirect(url_for("base"))
        
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

@bp.route("/<int:id>/update_password", methods=['GET', 'POST'])
@login_required
def update_password(id):
    if request.method == "POST":
        db, c = cnxn()
        password_anterior = request.form['password_anterior']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        c.execute('select * from Usuarios where id = ?', id)
        current_password = c.fetchone()
        error = None
        

        if not check_password_hash(current_password[2], password_anterior):
            error = "La contraseña ingresada no coincide con su contraseña actual"
        if password == password_anterior:
            error = "Su nueva contraseña no puede ser igual a la anterior"
        if password == password_confirm:
            pass
        else:
            error = "Verifique que las contraseñas ingresadas sean iguales"
        if error is None:
            c.execute("update Usuarios set contraseña = ? where id = ?", generate_password_hash(password), id)
            db.commit()
            logout()
            return redirect(url_for('auth.login'))
        flash(error)
    
    return render_template('auth/update_password.html')
