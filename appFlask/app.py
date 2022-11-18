from enum import auto
from os import path
from tkinter.filedialog import Open
from flask import Flask,request
from flask_cors import CORS
from flask_cors.core import serialize_option
import requests
import xml.etree.ElementTree as xml
import re
from xml.dom import minidom



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
@app.route("/resumenrango",methods=['GET'])
def resumenFechaRango():
    ar=xml.parse('auto.xml')
    r=ar.getroot()
    listaFechas=[]
    listaTotales=[]
    for d in r.findall('AUTORIZACION'):
        dt=d.find('FECHA').text
        solofecha=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(dt))
        solo=solofecha.group()
        for dti in d.findall('LISTADO_AUTORIZACIONES'):
            for dti2 in dti.findall('APROBACION'):
                tt=dti2.find('TOTAL').text
                tte=tt.strip()
                listaTotales.append(tte)
        listaFechas.append(solo)
    j={
        'FECHA':listaFechas,
        'TOTAL':listaTotales
    }
    return j

@app.route("/inicio/envio",methods=['GET'])
def salida():
    archivo=open('autorizaciones.xml')
    xmltexto=archivo.read()
    print(xmltexto)
    text={
        'archivo':xmltexto
    }

    return text

def cantidadFechas():
    contadorFechA=0
    cont=0
    print("aqui si entro"+str(cont))
    archi=xml.parse('auto.xml')
    archi2=xml.parse('auto.xml')
    root=archi.getroot()
    root2=archi2.getroot()
    uno=""
    
    for dte in root.findall('AUTORIZACION'):
        for tiempo in dte.findall('FECHA'):
            fecha=tiempo.text
            expresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fecha))
            exp=expresion.group()
            cont=cont+1
    print("cantidad de fechas "+str(cont))
    return cont

def obtenerfecha(posicion):
    contadorFechA=0
    archi=xml.parse('auto.xml')
    root=archi.getroot()
    exp=""
    for dte in root.findall('AUTORIZACION'):
        for tiempo in dte.findall('FECHA'):
            contadorFechA=contadorFechA+1
            print(contadorFechA)
            if contadorFechA==posicion:
                fecha=tiempo.text
                expresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fecha))
                exp=expresion.group()
    print("fecha obtenida"+str(exp))
    return exp
                

@app.route("/fechas",methods=['GET'])
def fechas():
    fe=cantidadFechas()
    lista = []
    for num in range(1,cantidadFechas()+1):
        lista.append(obtenerfecha(num))
    conx={
        'cantidadFechas':lista,
    }
    print(conx)
    return conx
    
    


@app.route("/proceso", methods=['POST'])
def proceso():    
    texto = request.data.decode('utf-8')
    print(texto)
    file=open("prueba.xml",'w')
    file.write(texto)
    file.close()
    xmll=xml.parse('prueba.xml')
    xml2=xml.parse('prueba.xml')
    xml3=xml.parse('prueba.xml')
    xml4=xml.parse('prueba.xml')
    root1=xmll.getroot()
    root2=xml2.getroot()
    root3=xml3.getroot()
    root4=xml4.getroot()
    contador=0
    errorNitEmisor=0
    errorNitReceptor=0
    errorIva=0
    errortotal=0
    errorDuplicada=0
    refNum=""
    raiz=xml.Element('LISTAAUTORIZACIONES')
    exp2=""
    for dte in root1.findall('DTE'):
        for tiempo in dte.findall('TIEMPO'):
            fecha=tiempo.text
            expresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fecha))
            exp=expresion.group()
            if exp!=exp2: 
                
                for dte2 in root2.findall('DTE'):
                    for tiemp in dte2.findall('TIEMPO'):
                        fech=tiemp.text
                        expresion2=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fech))
                        expresion3=expresion2.group()
                        
                        if expresion3==exp:
                            contador=contador+1
                
                autorizaciones=xml.SubElement(raiz,'AUTORIZACION')
                fecha=xml.SubElement(autorizaciones,'FECHA')
                fecha.text=str(exp)
                facturas=xml.SubElement(autorizaciones,'FACTURAS_RECIBIDAS')
                facturas.text=str(contador)

                errores=xml.SubElement(autorizaciones,'ERRORES')#creacion de etiqueta errores
                emisor=xml.SubElement(errores,'NIT_EMISOR')#creacion de etiqueta nit emisor dentro de errores
                #metodo de encontrar errores de nit emisor
                
                for m in root1.findall('DTE'):
                    for nn in m.findall('TIEMPO'):
                        fAcomparar=nn.text
                        fExpresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fAcomparar))
                        fgroup=fExpresion.group()
                        if exp==fgroup:
                            nit=m.find('NIT_EMISOR').text
                            nitSinEspacios=nit.lstrip()
                            nitsinespacios2=nitSinEspacios.rstrip()
                            
                            longitud=len(nitsinespacios2)#OBTENGO LA LONGITUD DEL NIT
                            
                            letras=re.search(r"\D+",str(nitsinespacios2))#ver si tiene letras
                            
                            if longitud>20 or letras!=None:
                                errorNitEmisor=errorNitEmisor+1
                                
                            
                            expresionNitE=re.findall(r"[0-9]+",str(nit))#obtener solo los numero del nit
                            eNe=""
                            for n in range(0,len(expresionNitE)):
                                t=expresionNitE[n]
                                eNe=str(eNe)+str(t)
                            #print(eNe)#IMPRIMO EL NIT EN SOLO NUMEROS
                emisor.text=str(errorNitEmisor)          
                
                #-------------------------------------------------------------------------------------------
                #nitEmisor= dte.find('NIT_EMISOR').text #obtener el texto nit emisorde la etiqueta
                #print(str(nitEmisor))
                #longitud=len(nitEmisor) #longitur del nit obtenido
                #print(longitud)
                #expresionNitEmisor=re.findall(r"[0-9]+",str(nitEmisor))#obtener solo los numero del nit
                #eNe=""
                #for n in range(0,len(expresionNitEmisor)):
                #    t=expresionNitEmisor[n]
                #    eNe=str(eNe)+str(t)
                #print(eNe)
                #tieneLetras=re.search(r"\D+",str(nitEmisor))
                #print(tieneLetras.group())
                #for num in range(1,3):
                #    if num==1:
                #        for emi in root1.findall('DTE'):
                #            for emi2 in emi.findall("NIT_EMISOR"):
                #                dteee=emi2.text
                #                longitud=len(dteee)
                #                expresionNitEmisor=re.search(r"[0-9]+",str(dteee))
                #                tieneLetras=re.search(r"\D+",str(dteee))
                #                if len(expresionNitEmisor.group())>20 or len(tieneLetras.group())>0:
                #                    errorNitEmisor=errorNitEmisor+1
                #        errorn=xml.SubElement(errores,'NIT_EMISOR')
                #        errorn.text=str(errorNitEmisor)
                   
                #-----------------------------------------------------------------------------------------------
                receptor=xml.SubElement(errores,'NIT_RECEPTOR')
                #metodo de encontrar errores de nit emisor
                
                for m in root1.findall('DTE'):
                    for nn in m.findall('TIEMPO'):
                        fAcomparar=nn.text
                        fExpresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fAcomparar))
                        fgroup=fExpresion.group()
                        if exp==fgroup:
                            nit=m.find('NIT_RECEPTOR').text
                            nitSinEspacios=nit.lstrip()
                            nitsinespacios2=nitSinEspacios.rstrip()
                            #print("este es el nit a probar "+str(nitsinespacios2))
                            longitud=len(nitsinespacios2)#OBTENGO LA LONGITUD DEL NIT
                            #print("la longitud de este nit es "+str(longitud))
                            letras=re.search(r"\D+",str(nitsinespacios2))#ver si tiene letras
                            
                            if longitud>20 or letras!=None:
                                errorNitReceptor=errorNitReceptor+1
                                
                            
                            expresionNitE=re.findall(r"[0-9]+",str(nit))#obtener solo los numero del nit
                            eNe=""
                            for n in range(0,len(expresionNitE)):
                                t=expresionNitE[n]
                                eNe=str(eNe)+str(t)
                            #print(eNe)#IMPRIMO EL NIT EN SOLO NUMEROS
                receptor.text=str(errorNitReceptor)          
                
                #---------------------------------------------------------------------------------------------------
                iva=xml.SubElement(errores,'IVA')
                #metodo de encontrar errores de IVA
                for m in root1.findall('DTE'):
                    for nn in m.findall('TIEMPO'):
                        fAcomparar=nn.text
                        fExpresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fAcomparar))
                        fgroup=fExpresion.group()
                        if exp==fgroup:
                            #IVA TEXTO
                            datoIva=m.find('IVA').text
                            i=datoIva.strip()
                            valorD=m.find('VALOR').text
                            v=valorD.strip()
                            ii=float(i)
                            
                            vv=float(v)
                            
                            dato=round(vv*0.12,2)
                            
                            if dato==ii:
                                print("")
                            else:
                                errorIva=errorIva+1

                iva.text=str(errorIva)
                #-------------------------------------------------------------------------------------------
                total=xml.SubElement(errores,'TOTAL')
                #metodo de encontrar errores de total
                for m in root1.findall('DTE'):
                    for nn in m.findall('TIEMPO'):
                        fAcomparar=nn.text
                        fExpresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(fAcomparar))
                        fgroup=fExpresion.group()
                        if exp==fgroup:
                            #IVA TEXTO
                            datoIva=m.find('TOTAL').text
                            totall=datoIva.strip()
                            valorD=m.find('VALOR').text
                            v=valorD.strip()
                            i=m.find('IVA').text
                            ie=i.strip()
                            ii=float(ie)#iva float
                            
                            vv=float(v)#valor float
                            
                            tt=float(totall)#total float
                            
                            dato=vv+ii
                            
                            if round(dato,2)==round(tt,2):
                                print("")
                            else:
                                errortotal=errortotal+1

                total.text=str(errortotal)
                #-------------------------------------------------------------------------------------------
                duplicada=xml.SubElement(errores,'REFERENCIA_DUPLICADA')
                #metodo de encontrar errores de referencia duplicadas
                
                
                print("FECHA "+ str(exp))
                cout=""
                refNum
                for c in root3.findall('DTE'):
                    for q in c.findall('TIEMPO'):
                        qq=q.text
                        fExpresion=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(qq))
                        g=fExpresion.group()#fecha para comparar
                        if g==exp:#si fecha de primera lista es igual a la de la segunda
                            w=c.find('REFERENCIA').text
                            ww=w.strip()#referencia
                            if ww!=cout:
                                print("R1 "+ww)
                                for dte3 in root4.findall('DTE'):
                                    tiempo = dte3.find('TIEMPO').text
                                    fExpresio=re.search(r"[0-9]+/[0-9]+/[0-9]+",str(tiempo))
                                    referencia=fExpresio.group()#fecha
                                    o=dte3.find('REFERENCIA').text
                                    refsinEspacios=o.strip()#referencia
                                    print(refsinEspacios)
                                    if exp==referencia and ww==refsinEspacios:
                                        errorDuplicada=errorDuplicada+1
                                    refNum=refsinEspacios 
                        cout=ww
                                        
                duplicada.text=str(errorDuplicada)
                #autorizaciones=xml.SubElement(raiz,'AUTORIZACION')
                #fecha=xml.SubElement(autorizaciones,'FECHA')
                #fecha.text=str(exp)
                #facturas=xml.SubElement(autorizaciones,'FACTURAS_RECIBIDAS')
                #facturas.text=str(contador)
                #print("la fecha "+str(exp333)+" "+"esta "+str(contador)+" veces")
                #-------------------------------------------------------------------------------------------
                #FacCorrectas= xml.SubElement(autorizaciones,'FACTURAS_CORRECTAS')
                #CanEmisores=xml.SubElement(autorizaciones,'CANTIDAD_EMISORES')
                #CanReceptores=xml.SubElement(autorizaciones,'CANTIDAD_RECEPTORES')
                #ListadoAuto=xml.SubElement(autorizaciones,'LISTADO_AUTORIZACIONES')
                #Aprobacion=xml.SubElement(ListadoAuto,'APROBACION')
                
                contador=0
                errorNitEmisor=0
                errorNitReceptor=0
                errorIva=0
                errortotal=0
                
                
            exp2=exp
                 
    myraiz=xml.ElementTree(raiz)
    myraiz.write('autorizaciones.xml')
    file=open('autorizaciones.xml')
    file.close()
    
    algo={
        'mensaje':"archivo de entrada procesado"
    }
    return algo


@app.route("/registro",methods=['POST'])
def registro():
    datos = request.json['name']
    return datos
    
if __name__=="__main__": #FORMA RECOMENDADA MIENTRAS SE ESTA TRABAJANDO LA APLICACION
    app.run(debug=True)
#para correr el servidor: python tutorial.py