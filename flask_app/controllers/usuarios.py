from flask import render_template, session,redirect, request,flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.servicio import Servicio


bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    is_valid = Usuario.validate_user(request.form)

    if not is_valid:
        return redirect("/")
    new_user = {
        "nombre": request.form["nombre"],
        "apellido_paterno": request.form["apellido_paterno"],
        "apellido_materno": request.form["apellido_materno"],
        "email": request.form["email"],
        "contraseña": bcrypt.generate_password_hash(request.form["contraseña"]),
    }
    id = Usuario.save(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    return redirect('/bienvenido')

@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = Usuario.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.contraseña,request.form['contraseña']):
        flash("Invalid Email/Password","login")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/bienvenido')

@app.route("/bienvenido")
def bienvenido():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    usuario = Usuario.get_by_id(data)
    return render_template("bienvenido.html", usuario=usuario)

@app.route("/servicios")
def servicios():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template("servicios.html")

@app.route("/perfil")
def perfil():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    usuario = Usuario.get_by_id(data)
    uws = Usuario.usuarios_con_servicios()
    return render_template("perfil.html", usuario = usuario, uws = uws)

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    # data = {
    #     "id": session['user_id']
    # }
    uws = Usuario.usuarios_con_servicios()
    return render_template("dashboard.html", uws = uws)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')