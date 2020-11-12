import pyodbc

import click
from flask import current_app, g
from flask.cli import with_appcontext
#from .schema import instructions

server = "LAPTOP-P98FD85V"
database = "App_web"
username = "Nico"
password = "1234"

def cnxn():
    if 'db' not in g:
        g.db = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + server + "; Database=" + database 
        + ";UID=" + username + "; PWD="+ password)
        
    # OK! conexión exitosa
        g.c = g.db.cursor()
        
    print ("conexion exitosa")
    return g.db, g.c

# def cnxn():
#     if 'db' not in g:
#         g.db = pyodbc.connect(
#             host=current_app.config['DATABASE_HOST'],
#             user= current_app.config["DATABASE_USER"],
#             password= current_app.config["DATABASE_PASSWORD"],
#             database= current_app.config["DATABASE"]
#         )
#         g.c = g.db.cursor(dictionary=True)
#     return g.db, g.c

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)




