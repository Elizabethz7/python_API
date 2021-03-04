import flask #flask asigna solicitudes HTTP a funciones Python
from flask import request, jsonify 
#jsonify funcion que nos permite convertir listas y diccionarios a formato JSON

app = flask.Flask(__name__) #Crea el objeto de aplicación Flask
app.config["DEBUG"] = True  # Inicia el depurador, si la aplicacion tiene un formato incorrecto se vera un error


@app.route('/', methods=['GET']) #la ruta '/' la asignamos a una funcion home
def home():
    return "<h1>PRUEBA</h1>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books) #book seria una lista
@app.errorhandler(404) #si no existe la ruta
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run() #Uno de los metodos de la aplicacion Flask