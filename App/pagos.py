from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from App.auth import login_required
from App.db import cnxn

bp = Blueprint("pagos", __name__)
# @bp.route("/comprobantes_emitidos", methods=['GET'])
# @login_required
# def get_comprobantes_emitidos():
#     db, c = cnxn()
#     #error = None
#     c.execute("Select fecha, tipo, numero, nombre_receptor, total from comprobantes_emitidos")
#     comprobante = c.fetchall()
    

#     return render_template("pagos/comprobantes_emitidos.html", comprobante=comprobante)

@bp.route("/comprobantes_emitidos/<int:condicion1>/<int:condicion2>", methods=['GET','POST'])
def comprobantes_emitidos(condicion1, condicion2):
    db, c = cnxn()
    
    
    if request.method == "POST":
        pagados = request.form.get('pagados')
        if pagados == "Pagados":
            cond1 = 1
            cond2 = 1
        elif pagados == "No pagados":
            cond1 = 0
            cond2= 0
        else:
            cond1 = 0
            cond2 = 1
        
        return redirect(url_for("pagos.comprobantes_emitidos", condicion1 = cond1, condicion2 = cond2))
    c.execute("Select comprobantes_emitidos.fecha, tipo, numero, nombre_receptor, total, comprobantes_emitidos.id, pagado, pagos.forma_pago, pagos.fecha from comprobantes_emitidos left join pagos on comprobantes_emitidos.id = pagos.comprobante_emitido where pagado = ? or pagado = ?", condicion1, condicion2)
    comprobante = c.fetchall()

    return render_template("pagos/comprobantes_emitidos.html", comprobante=comprobante)

@bp.route("/<int:id>/pago", methods=["GET","POST"])
@login_required
def pago(id):
    db, c = cnxn()
    c.execute("select total from comprobantes_emitidos where id = ?", id)
    monto = c.fetchone()
    if request.method == "POST":
        fecha = request.form['fecha']
        importe = int(request.form['importe'])
        retIIBB = int(request.form['retIIBB'])
        retGcia = int(request.form['retGcia'])
        retIVA = int(request.form['retIVA'])
        retSUSS = int(request.form['retSUSS'])
        formaPago = request.form['forma de pago']
        print(formaPago)
        total = importe + retIIBB + retGcia + retIVA + retSUSS
        values = (fecha, importe, retIIBB, retGcia, retIVA, retSUSS, id,formaPago)
        c.execute("insert into pagos values (?,?,?,?,?,?,?,?)", values)
        db.commit()
        if total == monto[0]:
            c.execute("update comprobantes_emitidos set pagado = 1 where id = ?", id)
            db.commit()
        return redirect(url_for('pagos.comprobantes_emitidos', condicion1=0, condicion2=0))
    
    

    return render_template("pagos/pago.html")
    