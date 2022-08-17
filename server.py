from flask_app import app
from flask_app.controllers import servicios, usuarios, evaluaciones

if __name__=="__main__":
    app.run(debug=True)