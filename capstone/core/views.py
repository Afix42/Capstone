from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    # Datos para el slideshow y hero banner, puedes sustituirlos por modelos si los tienes
    slides_range = range(1, 4)  # Rango de ejemplo para el slideshow
    images = range(1, 4)  # Rango de ejemplo para las imágenes del hero banner

    # Renderiza la página principal con los datos del slideshow y hero banner
    return render(request, 'core/home.html', {
        'slides_range': slides_range,
        'images': images
    })

def register(request):
    return render(request, 'core/form_registro.html')  # Página de registro

def login(request):
    return render(request, 'core/form_login.html')  # Página de inicio de sesión

def foro(request):
    return render(request, 'core/foro.html')  # Página del foro

def tienda(request):
    # Aquí puedes agregar lógica para listar productos si tienes un modelo de productos
    return render(request, 'core/tienda.html')  # Página de la tienda

def vista_usuario(request):
    return render(request, 'core/home_usuario')

def vista_admin(request):
    return render(request, 'core/home_admin')