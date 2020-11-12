from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from App.auth import login_required
from App.db import cnxn

bp = Blueprint("arreglos", __name__)

@bp.route('/<int:id>/index')
@login_required
def index(id):
    db, c = cnxn()
    c.execute("Select * from Equipos where id=?", id)
    equipos=c.fetchone()
    #c.execute("select Arreglos.FechaArreglo, Equipos.Equipo, Locales.Local, Arreglos.Proveedor, Arreglos.Monto from Arreglos left join Equipos on Arreglos.Equipo = Equipos.id left join Locales on Equipos.local = Locales.id order by Arreglos.FechaArreglo")
    c.execute("select * from Arreglos where Equipo=?", id)
    arreglos = c.fetchall()

    return render_template('arreglos/index.html', arreglos=arreglos, equipos=equipos)

@bp.route('/<int:id>/cargar1', methods=['GET', 'POST'])
@login_required
def cargar1(id):
    db, c = cnxn()
    if request.method == 'POST':
        Fecha = request.form['Fecha']
        Proveedor = request.form['Proveedor']
        Monto = request.form['Monto']
        Descripcion = request.form['Descripcion']
        consulta = "Insert into Arreglos values (?, ?, ?, ?, ?)"
        values = (Fecha, id, Proveedor, Monto, Descripcion)
        c.execute(consulta, values)
        db.commit()

        return redirect(url_for('equipos.inicio'))

    return render_template('arreglos/cargar1.html')

