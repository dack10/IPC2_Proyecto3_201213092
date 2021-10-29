from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest
import requests

from tkinter import filedialog
import xml.etree.ElementTree as xml



# Create your views here.
url='http://localhost:5000/'
url2='http://localhost:8000/'
def inicio(request):
    return HttpResponse('Esto es un ejemplo ipc2')

def inicio2(request):
    return render(request,'app/index.html')

def inicio3(request):
    return render(request,'app/index.html')

def DatosE(request):
    return render(request,'app/DatosE.html')

def login(request):
    if request.method=='POST':
        algo={
            'name': request.POST['nombreUsuario'],
            'password': request.POST['contrasena']
        }
        r= requests.post(url+'procesar',json=algo,verify=True)
        print(r.text)
    return render(request,'app/login.html')

def registro(request):
    if request.method=='POST':
        algo={
            'name': request.POST['nombreUsuario'],
            'password': request.POST['contrasena']
        }
        r= requests.post(url+'registro',json=algo,verify=True)
        print(r.text)
    return render(request,'app/registro.html')

def leer(request):
    print(request.POST['entrada'])
    return render(request,'app/login.html')

def cargar(request):
    r= requests.post(url2+'cargar')
    archivo = filedialog.askopenfilename(title="abrir")
    