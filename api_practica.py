import flask #flask asigna solicitudes HTTP a funciones Python
from flask import request, jsonify, make_response 
from flask_cors import CORS
#jsonify funcion que nos permite convertir listas y diccionarios a formato JSON
import logging
import boto3
from botocore.exceptions import ClientError
import sys
import os
import mysql.connector
import hashlib
import uuid
import json
import base64
# AWS Autenticacion
ENDPOINT="database-semi1-p1.clhh689knnbh.us-east-2.rds.amazonaws.com"
PORT="3306"
USR="admin"
REGION="us-east-2"
DBNAME="ugramdb"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
#session = boto3.Session(profile_name='default')
client = boto3.client('rds') #La clave de sesión para su cuenta de AWS. Esto solo es necesario cuando utiliza credenciales temporales

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)                    
#aws
sesion_S3 = boto3.Session(
    aws_access_key_id="AKIAW2K5TQDRQRMQMOSK",
    aws_secret_access_key="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",
    region_name="us-east-2"
)
s3_client = boto3.client('s3')
#flask
app = flask.Flask(__name__) #Crea el objeto de aplicación Flask
app.config["DEBUG"] = True  # Inicia el depurador, si la aplicacion tiene un formato incorrecto se vera un error
CORS(app)

@app.route('/', methods=['GET']) #la ruta '/' la asignamos a una funcion home
def home():
    return "<h1>PRUEBA</h1>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
"""
    USUARIOS
"""
#encriptar
def encriptar(str_):
    result = hashlib.md5(str_.encode()) 
    return result.hexdigest()
#todos los usuarios
@app.route('/api/usuario', methods=['GET']) 
def usuarios_get_all():
    cur.execute("""SELECT * from usuario""")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    query_results = cur.fetchall()
    #return make_response(jsonify(query_results))
    json_data=[]
    for result in query_results:
        json_data.append(dict(zip(row_headers,result)))
    return make_response((json.dumps(json_data)))

#obtener un usuario
@app.route('/api/usuario/<id_user>', methods = ['GET']) 
def usuarios_get_one(id_user):
    cur.execute("SELECT * from usuario where id =%s" % (id_user))
    query_results = cur.fetchall()
    json_ = jsonify(query_results)
    if cur.rowcount == 0 :
        return make_response(jsonify({"error": "Not results"}), 404)
    return make_response(json_)
#crear usuario
@app.route('/api/usuario/', methods = ['POST']) 
def usuarios_create():
    data = request.get_json()
    try:
        pwd= encriptar(data['pwd'])
        cur.execute("INSERT INTO usuario(usuario,nombre,pwd) VALUES( '%s', '%s', '%s')" % (data['usuario'],data['nombre'],pwd))
        conn.commit()
        return make_response(jsonify({"usuario": data['usuario']}),200)
    except Exception as e:
        return make_response(jsonify({"error": "Problem inserting into db: " + str(e)}), 404)
#modificar usuario
@app.route('/api/usuario/', methods = ['PUT']) 
def usuarios_put():
    data = request.get_json()
    try:
        pwd= encriptar(data['pwd'])
        cur.execute("UPDATE usuario SET usuario = '%s',nombre = '%s', pwd = '%s' WHERE id = %s" % (data['usuario'],data['nombre'],pwd,data['id']))
        conn.commit()
        return make_response(jsonify({"usuario": data['usuario']}),201)
    except Exception as e:
        return make_response(jsonify({"error": "Problem updating into db: " + str(e)}), 404)
#login
@app.route('/api/login', methods = ['POST']) 
def login():
    data = request.get_json()
    pwd= encriptar(data['pwd'])
    cur.execute("SELECT * from usuario where usuario ='%s'" % (data['usuario']))
    row_headers=[x[0] for x in cur.description]
    query_results = cur.fetchall() #el resultado devuelve una lista
    #json_ = jsonify(json.loads(json.dumps(query_results))[0])
    json_ = json.loads(json.dumps(query_results))[0]
    if cur.rowcount == 0 :
        return make_response(jsonify({"error": "No se encontro coincidencia"}), 404)
    if json_[3] != pwd:
        return make_response(jsonify({"error": "Contraseña invalida"}), 404)
    #return make_response(json_)
    return make_response(jsonify({row_headers[0]:json_[0],row_headers[1]:json_[1],row_headers[2]:json_[2]
    ,row_headers[3]:json_[3],row_headers[4]:json_[4]}), 200)
"""
    ALBUM
"""
#albumnes de un usuario
@app.route('/api/album/<id_user>', methods = ['GET']) 
def album_one(id_user):
    cur.execute("SELECT * FROM album WHERE user_ =%s" % (id_user))
    row_headers=[x[0] for x in cur.description]
    query_results = cur.fetchall()
    json_ = jsonify(query_results)
    if cur.rowcount == 0 :
        return make_response(jsonify({"error": "Not results"}), 404)
    json_data=[]
    for result in query_results:
        json_data.append(dict(zip(row_headers,result)))
    return make_response((json.dumps(json_data)))
#crear album
@app.route('/api/album/', methods = ['POST']) 
def album_create():
    data = request.get_json()
    try:
        cur.execute("INSERT INTO album(nombre,user_) VALUES('%s', '%s')" % (data['nombre'],data['id_usuario']))
        conn.commit()
        return make_response(jsonify({"nombre": data['nombre'],"id_usuario": data['id_usuario']}),200)
    except Exception as e:
        return make_response(jsonify({"error": "Problem inserting into db: " + str(e)}), 404)

#eliminar album
@app.route('/api/album/<id>', methods = ['DELETE']) 
def album_delete(id):
    try:
        cur.execute("DELETE FROM album WHERE id = '%s'" % (id))
        conn.commit()
        return make_response(jsonify({"album":id}),201)
    except Exception as e:
        return make_response(jsonify({"error": "Problem deleting into db: " + str(e)}), 404)

"""
    FOTOS
"""
#obtener una foto
@app.route('/api/foto/<id_user>', methods = ['GET']) 
def foto_one(id_user):
    cur.execute("SELECT * FROM foto WHERE id =%s" % (id_user))
    row_headers=[x[0] for x in cur.description]
    query_results = cur.fetchall()
    json_ = json.loads(json.dumps(query_results))[0]
    if cur.rowcount == 0 :
        return make_response(jsonify({"error": "Not results"}), 404)
    return make_response(jsonify({row_headers[0]:json_[0],row_headers[1]:json_[1],row_headers[2]:json_[2]
    ,row_headers[3]:json_[3]}), 200)
#obtener fotos de un album
@app.route('/api/album_foto/<id_user>', methods = ['GET']) 
def fotos_album(id_user):
    cur.execute("SELECT * FROM foto WHERE album =%s" % (id_user))
    row_headers=[x[0] for x in cur.description]
    query_results = cur.fetchall()
    json_ = jsonify(query_results)
    if cur.rowcount == 0 :
        return make_response(jsonify({"error": "Not results"}), 404)
    json_data=[]
    for result in query_results:
        json_data.append(dict(zip(row_headers,result)))
    return make_response((json.dumps(json_data)))
#crear fotos
@app.route('/api/foto/', methods = ['POST']) 
def foto_create():
    data = request.get_json()
    #try:
    filename= data['nombre'] + '-' + str(uuid.uuid1()) + '.' + data['extension']
    message_bytes = base64.b64decode(data['base64'])
    #upload_file(str(filename),"practica1-g17-imagenes",str(message_bytes))
    s3 = boto3.resource('s3')
    s3.Bucket("practica1-g17-imagenes").put_object(Key=filename, Body=message_bytes,ContentType='image/png',ACL='public-read')

        #cur.execute("INSERT INTO usuario(usuario,nombre,pwd) VALUES( '%s', '%s', '%s')" % (data['usuario'],data['nombre'],pwd))
        #conn.commit()
        #return make_response(jsonify({"usuario": data['usuario']}),200)
    #except Exception as e:
        #return make_response(jsonify({"error": "Problem inserting into db: " + str(e)}), 404)
    return make_response(jsonify({"usuario": "wenas"}),200)
def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: location-of-your-file
    :param bucket: Bucket to upload to
    :param object_name: S3 object name name-of-file-in-s3se
    """
    # Upload the file
   
    try:
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read','ContentType': 'Image'})
    except ClientError as e:
        logging.error(e)
        return False
    return True
def upload_(file_name, bucket, object_name):
    s3 = boto3.resource('s3')
    s3.Bucket("practica1-g17-imagenes").put_object(Key=filename, Body=message_bytes,ContentType='image/png',ACL='public-read')
   #aws
    sesion_S3 = boto3.Session(
        aws_access_key_id="AKIAW2K5TQDRQRMQMOSK",
        aws_secret_access_key="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",
        region_name="us-east-2"
    )
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name,ExtraArgs={'ACL': 'public-read','ContentType': 'Image'})
    except ClientError as e:
        logging.error(e)
        return False
    return True
if __name__ == "__main__":
    try:
        conn =  mysql.connector.connect(host=ENDPOINT, user=USR, passwd='12345678', port=PORT, database=DBNAME)
        cur = conn.cursor()
        cur.execute("""SELECT * from foto""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))
    app.run() #Uno de los metodos de la aplicacion Flask
