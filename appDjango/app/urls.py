from django.urls import path
from django.urls.resolvers import URLPattern
from .views import DatosE, cargar, inicio, inicio3, leer, login,registro,prueba,mostrarSalida,mostrarFechas,mostrarRango
urlpatterns = [
    path('',inicio),
    path('login',login),
    path('inicio/envio',mostrarSalida),
    path('inicio/fecha',mostrarFechas),
    path('inicio/rango',mostrarRango),
    path('inicio',prueba),
    path('index.html',inicio3),
    path('DatosE.html',DatosE),
    path('cargar',cargar),
    path('leer',leer),
    path('registro',registro)
    
    
]
