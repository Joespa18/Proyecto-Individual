from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app.models import servicio

class Usuario:
    db = 'encuentralo'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido_paterno = data['apellido_paterno']
        self.apellido_materno = data['apellido_materno']
        self.email = data['email']
        self.contraseña = data['contraseña']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido_paterno,apellido_materno, email, contraseña) VALUES (%(nombre)s,%(apellido_paterno)s,%(apellido_materno)s,%(email)s,%(contraseña)s);"
        return connectToMySQL (cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def categoria_taxi(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id WHERE categoria = 'taxi';"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    @classmethod
    def categoria_taxi(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id WHERE categoria = 'taxi';"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    @classmethod
    def categoria_gasfiter(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id WHERE categoria = 'gasfiter';"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    @classmethod
    def categoria_electricista(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id WHERE categoria = 'electricista';"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    @classmethod
    def categoria_maestro(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id WHERE categoria = 'maestro';"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     results = connectToMySQL(cls.db).query_db(query)
    #     users = []
    #     for row in results:
    #         users.append( cls(row) )
    #     return users 

    @classmethod
    def usuarios_con_servicios(cls):
        query = "SELECT usuarios.id, usuarios.nombre, apellido_paterno, apellido_materno, email, contraseña, usuarios.created_at, usuarios.updated_at, servicios.id as servicio_id, telefono, categoria, descripcion, servicios.created_at, servicios.updated_at, usuario_id FROM usuarios JOIN servicios ON usuarios.id = servicios.usuario_id;"
        results = connectToMySQL(cls.db).query_db(query)
        foundings= []
        for row in results:
            foundings.append( cls(row) )
        return results

    @staticmethod
    def validate_user(usuario):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(Usuario.db).query_db(query,usuario)
        if len(usuario['nombre']) < 2:
            is_valid = False
            flash("El nombre debe tener al menos 2 caracteres","register")
        if len(usuario['apellido_paterno']) < 2:
            is_valid = False
            flash("El apellido paterno debe tener al menos 2 caracteres","register")
        if len(usuario['apellido_materno']) < 2:
            is_valid = False
            flash("El apellido materno debe tener al menos 2 caracteres","register")
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Ingresa un email válido","register")
        if len(usuario['contraseña']) < 8:
            is_valid = False
            flash("La contraseña debe tener al menos 8 caracteres","register")
        if usuario['contraseña'] != usuario['confirm']:
            is_valid = False
            flash("Las contraseñas no coinciden!","register")
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        return is_valid