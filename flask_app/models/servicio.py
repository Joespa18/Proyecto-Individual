from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Servicio:
    db = 'encuentralo'
    def __init__(self, data):
        self.id = data['id']
        self.telefono = data['telefono']
        self.categoria = data['categoria']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO servicios (categoria, telefono, descripcion, usuario_id) VALUES (%(categoria)s, %(telefono)s, %(descripcion)s, %(usuario_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM bands;"
    #     results =  connectToMySQL(cls.db).query_db(query)
    #     all_bands = []
    #     for row in results:
    #         all_bands.append( cls(row) )
    #     return all_bands
    

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM bands WHERE id = %(id)s;"
    #     result =connectToMySQL(cls.db).query_db(query, data)
    #     return cls(result[0])

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE bands SET band_name=%(band_name)s, music_genre=%(music_genre)s, home_city=%(home_city)s WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db).query_db(query, data)

    # @classmethod
    # def destroy(cls,data):
    #     query = "DELETE FROM bands WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db).query_db(query,data)

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