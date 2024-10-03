# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Nueva URL para la plantilla de registro
    path('login/', views.login, name='login'),  # Nueva URL para la plantilla de registro
    path('foro/', views.foro, name='foro'),  # Nueva URL para la plantilla de registro
    path('tienda/', views.tienda, name='tienda'),  # Nueva URL para la plantilla de registro
    path('usuario/', views.vista_usuario, name='usuario'),
    path('admin/',views.vista_admin, name='admin'),
]