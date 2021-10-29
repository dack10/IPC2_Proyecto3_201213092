from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__) 
#CREAMOS UNA INSTANCIA DE ESTA CLASE EL ARGUMENTO QUE SE LE PASA ES NAME POR QUE LA APP 
# NECESITA SABER SI ESTA SIENDO EJECUTADA DESDE UN ARCHIVO PRINCIPAL

CORS(app)

@app.route("/") #Esto va antes de la funcion
def index(): #creamos una funcion
    return "Hola,mundo"

#DEBEMOS DE CREAR UNA RUTA YA QUE ESTE ES EL SERVIDOR Y ASI SABEMOS A DONDE 
#SE TIENE QUE REDIRIGIR

@app.route("/procesar", methods=['POST'])
def procesar():
    algo={
            'name': request.json['password'],
            'password': request.json['name']
        }
    datos = request.json['password']
    datos2 = request.json['name']
    
    return algo

@app.route("/registro",methods=['POST'])
def registro():
    datos = request.json['name']
    return datos
    
if __name__=="__main__": #FORMA RECOMENDADA MIENTRAS SE ESTA TRABAJANDO LA APLICACION
    app.run(debug=True)
#para correr el servidor: python tutorial.py