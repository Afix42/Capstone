# urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # Esta es la ruta a la que necesitas apuntar
    path('foro/', views.foro, name='foro'),
    path('tienda/', views.tienda, name='tienda'),
    path('usuario/', views.vista_usuario, name='usuario'),
    path('admin/', views.vista_admin, name='admin'),
    path('registro/', views.registro_view, name='registro'),
    path('inicio_sesion/', views.funcion_login, name='login'),  # Esta es la función que maneja el login
    path('producto/', views.producto, name='producto'),    
    path('cerrar_sesion/', views.funcion_logout, name='cerrar_sesion'),
]
