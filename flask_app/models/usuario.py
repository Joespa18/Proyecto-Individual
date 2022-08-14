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

        self.servicios = []             #Aquí irán los serivicios de cada usuario, si es que tiene
    @classmethod
    def save(cls, data):
        query = """INSERT INTO usuarios (nombre, apellido_paterno,apellido_materno, email, contraseña) 
        VALUES (%(nombre)s,%(apellido_paterno)s,%(apellido_materno)s,%(email)s,%(contraseña)s);"""
        return connectToMySQL (cls.db).query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = """SELECT * FROM usuarios 
        LEFT JOIN servicios ON usuarios.id = servicios.usuario_id
        WHERE email = %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        for row in results:     
            if row['servicios.id']:
                data2 = {
                'id': row['servicios.id'],
                'telefono': row['telefono'],
                'categoria': row['categoria'],
                'descripcion': row['descripcion'],
                'updated_at': row['updated_at'],
                'created_at': row['created_at'],
                }
                user.servicios.append(servicio.Servicio(data2))
        return user

    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM usuarios 
        LEFT JOIN servicios ON usuarios.id = servicios.usuario_id
        WHERE usuarios.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        for row in results:     
            if row['servicios.id']:
                data2 = {
                'id': row['servicios.id'],
                'telefono': row['telefono'],
                'categoria': row['categoria'],
                'descripcion': row['descripcion'],
                'updated_at': row['updated_at'],
                'created_at': row['created_at'],
                }
                user.servicios.append(servicio.Servicio(data2))
        return user

    @classmethod
    def usuarios_con_servicios(cls):
        query = """SELECT * FROM usuarios;"""
        results = connectToMySQL(cls.db).query_db(query)
        users= []
        for row in results:
            users.append( cls(row) )    #Para obtener los usuarios con servicios primero pido todos los usuarios a la db y los convierto en instancias de clase Usuario
        for user in users:              #Luego, por cada usuario, hago una consulta a la db para sacar los servicios de cada usuario con un for loop
            query = f"SELECT * FROM usuarios LEFT JOIN servicios ON usuarios.id = servicios.usuario_id WHERE usuarios.id = {user.id};"
            results = connectToMySQL(cls.db).query_db(query) 
            if results:                 #Con este condicional me aseguro de que, si un usuario registrado no tiene servicios, no se ejecute este pedazo de código y no de error
                for row in results:     #Con este for loop, si un usuario da más de un servicio (Puede que sea gasfitero y electricista o más cosas), se asegura de que se pasen todos sus servicios como instancias de clase Servicio al array "self.servicios = []" de cada usuario.
                    data = {
                    'id': row['servicios.id'],
                    'telefono': row['telefono'],
                    'categoria': row['categoria'],
                    'descripcion': row['descripcion'],
                    'updated_at': row['updated_at'],
                    'created_at': row['created_at'],
                    }
                    user.servicios.append(servicio.Servicio(data))        #Al final, parseo los datos que son del servicio como variable data a crear instancias de servicios y añadirlas a "self.servicios = []"
        return users                    #Esto debería retornar una lista de todos los usuarios como objetos, cada uno con una lista de servicios, estos también como objetos.

    @staticmethod
    def validate_user(usuario):
        is_valid = True
        query = """SELECT * FROM usuarios WHERE email = %(email)s;"""
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

