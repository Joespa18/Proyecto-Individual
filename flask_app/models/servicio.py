from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import usuario

class Servicio:
    db = 'encuentralo'
    def __init__(self, data):
        self.id = data['id']
        self.telefono = data['telefono']
        self.categoria = data['categoria']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    @classmethod
    def save(cls, data):
        query = """INSERT INTO servicios (categoria, telefono, descripcion, usuario_id) 
        VALUES (%(categoria)s, %(telefono)s, %(descripcion)s, %(usuario_id)s);"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_category(cls , data):
        query = """SELECT * FROM servicios
        WHERE servicios.categoria = %(categoria)s;
        """
        results = connectToMySQL(cls.db).query_db(query , data)
        servicios = []
        for row in results:
            servicios.append(cls(row))
        for s in servicios:
            query = f"SELECT * FROM servicios LEFT JOIN usuarios ON servicios.usuario_id = usuarios.id WHERE servicios.id = {s.id};"
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
                s.user = usuario.Usuario(data)
        return servicios
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM bands;"
    #     results =  connectToMySQL(cls.db).query_db(query)
    #     all_bands = []
    #     for row in results:
    #         all_bands.append( cls(row) )
    #     return all_bands
    

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM servicios WHERE id = %(id)s;"
        result =connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE servicios SET telefono=%(telefono)s, categoria=%(categoria)s, descripcion=%(descripcion)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM servicios WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_band(servicio):
        is_valid = True
        if len(servicio['telefono']) < 8:
            is_valid = False
            flash("por favor ingrese un número válido","servicio")
        if len(servicio['categoria']) < 1:
            is_valid = False
            flash("Escoja una de las categorias","servicio")
        if len(servicio['descripcion']) < 8:
            is_valid = False
            flash("Por favor ingrese una descripción de al menos 8 caracteres","servicio")
        return is_valid