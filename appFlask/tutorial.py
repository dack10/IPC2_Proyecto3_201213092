from enum import auto
from os import path
from tkinter.filedialog import Open
from flask import Flask,request
from flask_cors import CORS
from flask_cors.core import serialize_option
import requests
import xml.etree.ElementTree as xml
import re

app = Flask(__name__) 
#CREAMOS UNA INSTANCIA DE ESTA CLASE EL ARGUMENTO QUE SE LE PASA ES NAME POR QUE LA APP 
# NECESITA SABER SI ESTA SIENDO EJECUTADA DESDE UN ARCHIVO PRINCIPAL

CORS(app)

@app.route("/") #Esto va antes de la funcion
def index(): #creamos una funcion
    return "Hola,mundo 3"

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

@app.route("/proceso", methods=['POST'])
def proceso():    
    #texto = request.data.decode('utf-8')
    #print(texto)
    #file=open("prueba.xml",'w')
    #file.write(texto)
    #file.close()
    xmll=xml.parse('prueba.xml')
    xml2=xml.parse('prueba.xml')
    root1=xmll.getroot()
    root2=xml2.getroot()
    contador=0
    errorNitEmisor=0
    for dte in root1.findall('DTE'):
        for tiempo in dte.findall('TIEMPO'):
            fecha=tiempo.text
            expresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fecha))
            exp=expresion.group()
            print("elemento de lista "+exp)
            for dte2 in root2.findall('DTE'):
                for tiemp in dte2.findall('TIEMPO'):
                    fech=tiemp.text
                    expresion2=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fech))
                    expresion3=expresion2.group()
                    print("elemento de la otra lista para comparar "+expresion3)
                    if expresion3==exp:
                        contador=contador+1
        print(contador)
        contador=0  
    
    raiz=xml.Element('LISTAAUTORIZACIONES')
    #for num in range(0,3):
        #autorizaciones=xml.SubElement(raiz,'AUTORIZACION')
    exp2=""
    for dte in root1.findall('DTE'):
        for tiempo in dte.findall('TIEMPO'):
            fecha=tiempo.text
            expresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fecha))
            exp=expresion.group()
            if exp!=exp2: 
                print("elemento de lista "+exp)
                for dte2 in root2.findall('DTE'):
                    for tiemp in dte2.findall('TIEMPO'):
                        fech=tiemp.text
                        expresion2=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fech))
                        expresion3=expresion2.group()
                        print("elemento de la otra lista para comparar "+expresion3)
                        if expresion3==exp:
                            contador=contador+1
                print("la fecha "+str(exp)+" "+"esta "+str(contador)+" veces")
                autorizaciones=xml.SubElement(raiz,'AUTORIZACION')
                fecha=xml.SubElement(autorizaciones,'FECHA')
                fecha.text=str(exp)
                facturas=xml.SubElement(autorizaciones,'FACTURAS_RECIBIDAS')
                facturas.text=str(contador)
                errores=xml.SubElement(autorizaciones,'ERRORES')
                emisor=xml.SubElement(errores,'NIT_EMISOR')
                nitEmisor= dte.find('NIT_EMISOR').text
                print(str(nitEmisor))
                longitud=len(nitEmisor)
                expresionNitEmisor=re.search(r"[0-9]+",str(nitEmisor))
                tieneLetras=re.search(r"\D+",str(nitEmisor))
                print(tieneLetras.group())
                for num in range(1,3):
                    if num==1:
                        for emi in root1.findall('DTE'):
                            for emi2 in emi.findall("NIT_EMISOR"):
                                dteee=emi2.text
                                longitud=len(dteee)
                                expresionNitEmisor=re.search(r"[0-9]+",str(dteee))
                                tieneLetras=re.search(r"\D+",str(dteee))
                                if len(expresionNitEmisor.group())>20 or len(tieneLetras.group())>0:
                                    errorNitEmisor=errorNitEmisor+1
                        errorn=xml.SubElement(errores,'NIT_EMISOR')
                        errorn.text=str(errorNitEmisor)
                errorNitEmisor=0        

                receptor=xml.SubElement(errores,'NIT_RECEPTOR')
                iva=xml.SubElement(errores,'IVA')
                total=xml.SubElement(errores,'TOTAL')
                duplicada=xml.SubElement(errores,'REFERENCIA_DUPLICADA')
                print(str(contador))
                contador=0
            exp2=exp

                  
    print("error "+str(errorNitEmisor))
    myraiz=xml.ElementTree(raiz)
    myraiz.write('autorizaciones.xml')
    file=open('autorizaciones.xml')
    return 0


    

   
    
    


    

@app.route("/registro",methods=['POST'])
def registro():
    datos = request.json['name']
    return datos
    
if __name__=="__main__": #FORMA RECOMENDADA MIENTRAS SE ESTA TRABAJANDO LA APLICACION
    app.run(debug=True)
#para correr el servidor: python tutorial.py