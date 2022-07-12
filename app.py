from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

app= Flask(__name__)
app.secret_key='Develoteca'

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='bebidas alcoholicas'
mysql.init_app(app)

CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreEtiqueta>')
def uploads(nombreEtiqueta):
    return send_from_directory(app.config['CARPETA'], nombreEtiqueta)

@app.route('/')
def index():
    query='SELECT * FROM `vinos2`;'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(query)
    vinos=cursor.fetchall()
    conn.commit()
    return render_template("vinos/index.html", vinos=vinos)

@app.route('/create')
def create():
    return render_template('vinos/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _color=request.form['txtColor']
    _cepa=request.form['txtCepa']
    _bodega=request.form['txtBodega']
    _etiqueta=request.files['txtEtiqueta']

    if _nombre == '' or _color=='' or _cepa=='' or _bodega=='' or _etiqueta=='':
        flash('Llenar todos los campos')    
        return redirect(url_for('create'))

    now=datetime.now()
    tiempo= now.strftime("%Y-%H-%M-%S")
    if _etiqueta.filename != '':
        nuevoNombreEtiqueta= tiempo+_etiqueta.filename
        _etiqueta.save("uploads/"+nuevoNombreEtiqueta)

    query='INSERT INTO `bebidas alcoholicas`.`vinos2` (`ID`, `Nombre`, `Color`, `Cepa`, `Bodega`, `Etiqueta`) VALUES (NULL, %s, %s, %s, %s, %s);'
    datos=(_nombre, _color, _cepa, _bodega, nuevoNombreEtiqueta)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(query, datos)
    empleados=cursor.fetchall()
    conn.commit()
    return redirect('/')

@app.route('/destroy/<int:id>')
def destrot(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `bebidas alcoholicas`.`vinos2` WHERE id=%s",(id))
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("DELETE FROM `bebidas alcoholicas`.`vinos2` WHERE id=%s",(id))
    conn.commit()
    return redirect ('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM `bebidas alcoholicas`.`vinos2` WHERE id=%s",(id))
    vinos=cursor.fetchall()
    conn.commit()
    return render_template('vinos/edit.html', vinos=vinos)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _color=request.form['txtColor']
    _cepa=request.form['txtCepa']
    _bodega=request.form['txtBodega']
    _etiqueta=request.files['txtEtiqueta']
    id=request.form['txtID']
    query="UPDATE `bebidas alcoholicas`.`vinos2` SET `nombre`=%s, `color`=%s, `cepa`=%s, `bodega`=%s WHERE id=%s;"
    datos=(_nombre, _color, _cepa, _bodega, id) F

    #ACTUALIZACION DE FOTO SI ES NECESARIO
    conn=mysql.connect()
    cursor=conn.cursor()  
    now=datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _etiqueta.filename != '':
        nuevoNombreEtiqueta= tiempo+_etiqueta.filename
        _etiqueta.save("uploads/"+nuevoNombreEtiqueta)    
        cursor.execute("SELECT * FROM `bebidas alcoholicas`.`vinos2` WHERE id=%s",id)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `bebidas alcoholicas`.`vinos2` SET `etiqueta`=%s WHERE id=%s", (nuevoNombreEtiqueta, id))
        conn.commit()
    #ACA TERMINA LA ACTUALIZACION DE LA FOTO

    cursor.execute(query, datos)
    conn.commit() #ACA TERMINA LA FUNCION UPDATE

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
