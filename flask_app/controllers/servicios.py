from flask import render_template, session,redirect, request,flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.servicio import Servicio

@app.route('/crear')
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    usuario = Usuario.get_by_id(data)
    return render_template('crearServicio.html', usuario=usuario)

@app.route("/dashboard/<categoria>")
def dashboard(categoria):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    data2 = {
        "categoria" : categoria
    }
    usuario = Usuario.get_by_id(data)
    categoria1 = str(categoria)
    servicios = Servicio.get_by_category(data2)
    return render_template("dashboard.html", servicios = servicios, usuario = usuario, categoria = categoria1)

@app.route('/crear/servicio',methods=['POST'])
def nuevo_servicio():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Servicio.validate_band(request.form):
        return redirect('/crear')
    data = {
        "categoria": request.form["categoria"],
        "telefono": request.form["telefono"],
        "descripcion": request.form["descripcion"],
        "usuario_id": session["user_id"]
    }
    Servicio.save(data)
    return redirect(f"/dashboard/{request.form['categoria']}")