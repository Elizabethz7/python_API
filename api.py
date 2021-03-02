import flask #flask asigna solicitudes HTTP a funciones Python

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET']) #la ruta '/' la asignamos a una funcion home
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()
