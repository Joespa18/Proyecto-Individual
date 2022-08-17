from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import usuario

class Evaluacion:
    db = 'encuentralo'
    def __init__(self, data):
        self.id = data['id']
        self.comentario = data['comentario']
        self.evaluacion = data['evaluacion']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None
        self.receiever = None
    @classmethod
    def save(cls, data):
        query = """INSERT INTO evaluaciones (evaluacion, comentario, sender_id, receiver_id) 
        VALUES (%(evaluacion)s, %(comentario)s, %(sender_id)s, %(receiver_id)s);"""
        results = connectToMySQL(cls.db).query_db(query , data)
        print(results)
        return results

    @classmethod
    def get_all_of_one_by_user_id(cls , data):
        query = """SELECT * FROM evaluaciones 
        LEFT JOIN usuarios ON evaluaciones.sender_id = usuarios.id 
        WHERE receiver_id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query , data)
        evaluaciones = []
        if not results:
            return evaluaciones
        for row in results:
            evaluaciones.append(cls(row))
        for e in evaluaciones:
            query = f"SELECT * FROM evaluaciones LEFT JOIN usuarios ON evaluaciones.sender_id = usuarios.id WHERE evaluaciones.id = {e.id};"
            results = connectToMySQL(cls.db).query_db(query)
            for row in results:
                data = {
                    'id': row['usuarios.id'],
                    'nombre': row['nombre'],
                    'apellido_paterno': row['apellido_paterno'],
                    'apellido_materno': row['apellido_materno'],
                    'email': row['email'],
                    'contraseña': row['contraseña'],
                    'updated_at': row['usuarios.updated_at'],
                    'created_at': row['usuarios.created_at'],
                    }
                e.sender = usuario.Usuario(data)
        for e in evaluaciones:
            query = f"SELECT * FROM evaluaciones LEFT JOIN usuarios ON evaluaciones.receiver_id = usuarios.id WHERE evaluaciones.id = {e.id};"
            results = connectToMySQL(cls.db).query_db(query)
            for row in results:
                data = {
                    'id': row['usuarios.id'],
                    'nombre': row['nombre'],
                    'apellido_paterno': row['apellido_paterno'],
                    'apellido_materno': row['apellido_materno'],
                    'email': row['email'],
                    'contraseña': row['contraseña'],
                    'updated_at': row['usuarios.updated_at'],
                    'created_at': row['usuarios.created_at'],
                    }
                e.receiver = usuario.Usuario(data)
        # for e in evaluaciones:
        #     print(e.sender.id)
        return evaluaciones
