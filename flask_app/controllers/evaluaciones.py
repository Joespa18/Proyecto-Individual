from flask import render_template, session,redirect, request,flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.servicio import Servicio
from flask_app.models.evaluacion import Evaluacion

@app.route('/create/evaluacion/<int:receiver_id>',methods=['POST'])
def nueva_evaluacion(receiver_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if int(request.form["evaluacion"]) == 0:
        return redirect(f'/perfil/{receiver_id}')
    data = {
        "evaluacion": request.form["evaluacion"],
        "comentario": request.form["comentario"],
        "receiver_id": receiver_id,
        "sender_id": session['user_id'],
    }
    Evaluacion.save(data)
    return redirect(f"/perfil/{receiver_id}")