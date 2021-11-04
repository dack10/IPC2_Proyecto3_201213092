from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
import requests
import matplotlib.pyplot as plt

from tkinter import filedialog
import xml.etree.ElementTree as xml

from requests.sessions import Request
# Create your views here.
url = 'http://localhost:5000/'
url2 = 'http://localhost:8000/'


def inicio(request):
    return HttpResponse('Esto es un ejemplo ipc2')


def inicio2(request):
    return render(request, 'app/index.html')


def inicio3(request):
    return render(request, 'app/index.html')


def DatosE(request):
    return render(request, 'app/DatosE.html')
def grafica(request):
    plt.figure(figsize=(10,6))

    x = ["15/01/2021","15/01/2021","15/01/2021"]
    y=["25,52","256,10","41,25"]
    x2 = [2016,2017,2018,2019,2020,2021]
    y2=[40,41,42,43,44,45]

    plt.plot(x,y,marker='o',linestyle='--',color='r')
    plt.plot(x2,y2,marker='d',linestyle='--',color='r')
    plt.xlabel('FECHA')
    plt.ylabel('TOTAL')
    plt.title('RANGO')

    plt.yticks([45,48,51])

    plt.show()
   
    return render(request,'app/index.html')
def mostrarRango(request):
    if request.method=='GET':
        y=requests.get(url+"resumenrango",verify=True)
        con={
            'data':y.text
        }
        print(con)
    return render(request,"app/index.html",con)

def mostrarFechas(request):
    if request.method=='GET':
        o=requests.get(url+"fechas",verify=True)
        texto=o.text
        dataa={
            'fecha':texto
        }
        print(dataa)
    return render(request,'app/index.html',dataa)

def mostrarSalida(request):
    if request.method=='GET':
        u=requests.get(url+'inicio/envio',verify=True)
        kek=u.text
        print(u.text)
        archivo=open('C:/Users/DIEGO CULAJAY/OneDrive/Escritorio/Proyecto3/appFlask/auto.xml')
        s=archivo.read()
        archivo.close()
        
        data={
            "mensaje":s,
            'prueba':kek
        }
        
        print(s)
        print(data)
        return render(request,'app/index.html',data)

def login(request):
    if request.method == 'POST':
        algo = {
            'name': request.POST['nombreUsuario'],
            'password': request.POST['contrasena']
        }
        r = requests.post(url+'procesar', json=algo, verify=True)

        print(r.text)
    return render(request, 'app/login.html')
    
def prueba(request):
    if request.method == 'POST':
        
        r=request.POST['entrada']      
        
        r2 = requests.post(url+'proceso',data=r,verify=True)
        print(r2.text)
    return render(request,'app/index.html')


def registro(request):
    if request.method == 'POST':
        algo = {
            'name': request.POST['nombreUsuario'],
            'password': request.POST['contrasena']
        }
        r = requests.post(url+'registro', json=algo, verify=True)
        print(r.text)
    return render(request, 'app/registro.html')


def leer(request):
    print(request.POST['entrada'])
    return render(request, 'app/login.html')


def cargar(request):
    r = requests.post(url2+'cargar')
    archivo = filedialog.askopenfilename(title="abrir")
    r = request.POST['entrada']
    print(r)



    