from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_login
from .models import Usuario, Rol, Producto, TipoProducto
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.db import IntegrityError

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
    tipo_graficas = TipoProducto.objects.get(nombre_tipo='Graficas')  # Asegúrate de que 'Graficas' existe
    tipo_procesador = TipoProducto.objects.get(nombre_tipo='Procesador')
    tipo_placamadre = TipoProducto.objects.get(nombre_tipo='Placa Madre')
    productos_graficas = Producto.objects.filter(tipo_producto=tipo_graficas)  # Filtrar productos
    productos_procesador = Producto.objects.filter(tipo_producto=tipo_procesador)
    productos_placamadre = Producto.objects.filter(tipo_producto=tipo_placamadre)
    return render(request, 'core/tienda.html', {'productos': productos_graficas, 'procesadores': productos_procesador, 'placamadre': productos_placamadre})  # Pasar los productos a la plantilla

def vista_usuario(request):
    return render(request, 'core/home_usuario.html')

def vista_admin(request):
    return render(request, 'core/home_admin.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Usuario, Rol

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
                return redirect('login')  # Redirige a la página de inicio de sesión o donde prefieras
            except IntegrityError as e:
                # Si ocurre una violación de UNIQUE en el campo email
                if 'UNIQUE constraint' in str(e):
                    messages.error(request, 'El correo electrónico ya está registrado.')
                else:
                    messages.error(request, f'Error al registrar el usuario: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error inesperado: {str(e)}')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'core/form_registro.html')



from django.contrib.auth import authenticate, login as django_login
from core.models import Usuario  # Asegúrate de importar tu modelo de usuario
from django.shortcuts import render, redirect
from django.contrib import messages

def funcion_login(request):
    if request.method == 'POST':
        email = request.POST['email']  # Cambiar a 'email'
        password = request.POST['password']
        
        # Autenticar usando el email en lugar del username
        try:
            # Obtener el usuario basado en el email usando el modelo personalizado
            user = Usuario.objects.get(email=email)
            username = user.username  # Obtener el nombre de usuario asociado
            
            # Autenticar usando el nombre de usuario y la contraseña
            user = authenticate(request, username=username, password=password)
        except Usuario.DoesNotExist:
            user = None
        
        if user is not None:
            django_login(request, user)  # Esto debe estar correcto
            
            # Verifica si el usuario tiene rol de administrador
            if hasattr(user, 'rol') and user.rol.nombreRol == 'Administrador':
                print("Administrador inicio sesion")
                return redirect('home')  # Redirige a la vista de administrador
            else:
                print("Usuario inicio sesion")
                return redirect('home')  # Redirige a la vista de usuario
        else:
            messages.error(request, 'El usuario y/o contraseña no coinciden o no existen.')
            return render(request, 'core/form_login.html')

    return render(request, 'core/form_login.html')


def producto(request):
    return render(request, 'core/plantillas/producto.html')  # Página de la tienda

def funcion_logout(request):
    logout(request)  # Esta función cierra la sesión del usuario
    return redirect('home')  # Redirige a la página de inicio o cualquier otra página

