from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from App.auth import login_required
from App.db import cnxn

bp = Blueprint("equipos", __name__)
@bp.route('/inicio')
@login_required
def inicio():
    db, c = cnxn()
    error=None
    if g.user[3] == 1:
        c.execute("select * from Equipos where local = 1 order by Ubicación")
        equipos = c.fetchall()
    elif g.user[3] == 2:
        c.execute("Select * from Equipos where local = 2 order by Ubicación")
        equipos = c.fetchall()
    elif g.user[3] == 3:
        c.execute("Select * from Equipos")
        equipos = c.fetchall()
    else:
        c.execute("Select * from Equipos where local = 3")
        equipos = c.fetchall()
        error = "No puede consultar equipos - Solicite permisos al administrador"
        flash(error)
    return render_template('equipos/inicio.html', equipos=equipos)


@bp.route('/cargar', methods=['GET', 'POST'])
@login_required
def cargar():
    
    db, c = cnxn()
    if request.method == "POST":
        codigo = request.form['Codigo']
        equipo = request.form['Equipo']
        ubicacion = request.form['Ubicacion']
        
        error = None
        if g.user[3] == 1:
            c.execute("Select id from Equipos where codigo=? and equipo=? and local=?", codigo, equipo, 1)
            consulta=c.fetchone()
        elif g.user[3] == 2:
            c.execute("Select id from Equipos where codigo=? and equipo=? and local=?", codigo, equipo, 2)
            consulta=c.fetchone()
        else:
            error = "No tiene permiso para agregar equipos - consulte con el adminitrador"
            consulta = None
        if consulta is not None:
            error="El equipo {} ya se encuentra registrado".format(equipo)
        if error is None:
            if g.user[3] == 1:    
                agregarEquipo = 'insert into Equipos values (?, ?, ?, ?)'
                values= (codigo, ubicacion, 1, equipo)
                c.execute(agregarEquipo,values)
                db.commit()
            if g.user[3] == 2:    
                agregarEquipo = 'insert into Equipos values (?, ?, ?, ?)'
                values= (codigo, ubicacion, 2, equipo)
                c.execute(agregarEquipo,values)
                db.commit()

        #print (codigo, equipo, ubicacion, local, a[0])
        flash(error)
        return redirect(url_for('equipos.inicio'))

    return render_template("equipos/cargar.html")
