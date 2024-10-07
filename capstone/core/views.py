from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_login
from .models import Usuario, Rol
from django.contrib.auth.models import User
from django.contrib import messages

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
    return render(request, 'core/home_usuario.html')

def vista_admin(request):
    return render(request, 'core/home_admin.html')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['confirm_password']

        if password == repeat_password:
            try:
                # Crea un nuevo usuario utilizando la tabla Usuario
                user = Usuario.objects.create_user(username=username, email=email, password=password)
                
                # Asignar el rol predeterminado
                rol_predeterminado = Rol.objects.get(nombreRol='Usuario')  # Cambia 'Usuario' por el nombre de tu rol
                user.rol = rol_predeterminado
                user.save()  # Guarda los cambios del usuario
                
                # Mensaje de éxito
                messages.success(request, 'Usuario registrado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al registrar el usuario: {str(e)}')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'core/form_registro.html')


def funcion_login(request):
    if request.method == 'POST':
        username = request.POST['username']  # Cambiar 'nombre' a 'username'
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)  # Esto debe estar correcto
            # Verifica si el usuario tiene rol de administrador
            if hasattr(user, 'rol') and user.rol.nombreRol == 'Administrador':
                return redirect('admin')  # Redirige a la vista de administrador
            else:
                return redirect('usuario')  # Redirige a la vista de usuario
        else:
            messages.error(request, 'El usuario y/o contraseña no coinciden o no existen.')
            return render(request, 'core/form_login.html')

    return render(request, 'core/form_login.html')

def producto(request):
    return render(request, 'core/plantillas/producto.html')  # Página de la tienda