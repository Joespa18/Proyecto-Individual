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
    user = Usuario.get_by_id(data)
    return render_template('crearServicio.html', user=user)

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
    return redirect('/dashboard')

@app.route("/dashboard/taxi")
def dashboard_taxi():
    if 'user_id' not in session:
        return redirect('/')
    uws = Usuario.categoria_taxi()
    return render_template("dashboard.html", uws = uws)

@app.route("/dashboard/gasfiter")
def dashboard_gasfiter():
    if 'user_id' not in session:
        return redirect('/')
    uws = Usuario.categoria_gasfiter()
    return render_template("dashboard.html", uws = uws)

@app.route("/dashboard/electricista")
def dashboard_electricista():
    if 'user_id' not in session:
        return redirect('/')
    uws = Usuario.categoria_electricista()
    return render_template("dashboard.html", uws = uws)

@app.route("/dashboard/maestro")
def dashboard_maestro():
    if 'user_id' not in session:
        return redirect('/')
    uws = Usuario.categoria_maestro()
    return render_template("dashboard.html", uws = uws)