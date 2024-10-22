from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_login
from .models import Usuario, Rol, Producto, TipoProducto
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Usuario, Rol
from django.contrib.auth import update_session_auth_hash

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

@login_required
def perfil(request):
    user = request.user

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        foto_perfil = request.FILES.get('foto_perfil')  # Obtener la imagen

        # Actualizar los datos del usuario
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if foto_perfil:
            print("Nueva imagen subida:", foto_perfil)

        # Si se ha introducido una nueva contraseña, actualízala
        if password:
            user.set_password(password)

        # Actualizar la imagen si el usuario sube una nueva
        if foto_perfil:
            user.foto_perfil = foto_perfil

        # Guardar los cambios
        user.save()

        # Mensaje de éxito
        messages.success(request, 'Perfil actualizado con éxito.')

        # Redirigir a la misma página para evitar reenvío de formulario
        return redirect('perfil')
    
    return render(request, 'core/plantillas/perfil.html', {'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verificar que la contraseña actual es correcta
        if not request.user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('change_password')

        # Verificar que las nuevas contraseñas coincidan
        if new_password != confirm_password:
            messages.error(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('change_password')

        # Cambiar la contraseña
        request.user.set_password(new_password)
        request.user.save()

        # Mantener la sesión después de cambiar la contraseña
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
        return redirect('perfil')

    return render(request, 'core/plantillas/cambio_contra.html')


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

def funcion_logout(request):
    logout(request)  # Esta función cierra la sesión del usuario
    return redirect('home')  # Redirige a la página de inicio o cualquier otra página


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Preparar las imágenes del producto
    imagenes = [
        producto.imagen_uno.url if producto.imagen_uno else '/static/img/placeholder.jpg',
        producto.imagen_dos.url if producto.imagen_dos else '/static/img/placeholder.jpg',
        producto.imagen_tres.url if producto.imagen_tres else '/static/img/placeholder.jpg',
        producto.imagen_cuatro.url if producto.imagen_cuatro else '/static/img/placeholder.jpg',
    ]

    return render(request, 'core/plantillas/producto.html', {'producto': producto, 'imagenes': imagenes})


def compara(request):
    # Obtener todos los tipos de productos
    tipos = TipoProducto.objects.all()  
    productos = Producto.objects.all()  

    # Obtener IDs de los tipos seleccionados desde el formulario
    tipo_producto1_id = request.GET.get('tipo_producto1')
    tipo_producto2_id = request.GET.get('tipo_producto2')

    # Filtrar productos basados en los tipos seleccionados
    productos1 = Producto.objects.filter(tipo_producto_id=tipo_producto1_id) if tipo_producto1_id else []
    productos2 = Producto.objects.filter(tipo_producto_id=tipo_producto2_id) if tipo_producto2_id else []

    # Mostrar información sobre los productos filtrados
    return render(request, 'core/compara.html', {
        'tipos': tipos,
        'productos': productos,
        'productos1': productos1,
        'productos2': productos2,
    })





def comprobar_compatibilidad(request):
    if request.method == 'GET':
        id_producto1 = request.GET.get('producto1')
        id_producto2 = request.GET.get('producto2')

        if id_producto1 and id_producto2:
            producto1 = get_object_or_404(Producto, id=id_producto1)
            producto2 = get_object_or_404(Producto, id=id_producto2)

            mensaje = ""
            es_compatible = False

            def comprobar_socket(prod1, prod2):
                """Verifica si dos productos son compatibles según el socket."""
                if prod1.socket and prod2.socket:
                    sockets_prod1 = [socket.strip() for socket in prod1.socket.split(',')]
                    sockets_prod2 = [socket.strip() for socket in prod2.socket.split(',')]
                    return any(socket in sockets_prod2 for socket in sockets_prod1)
                return False

            def comparar_productos(prod1, prod2):
                """Función para comparar los productos en cualquier orden."""
                # Comparación entre procesador y placa madre (por el socket)
                if prod1.tipo_producto.nombre_tipo == 'Procesador' and prod2.tipo_producto.nombre_tipo == 'Placa Madre':
                    es_compatible = comprobar_socket(prod1, prod2)
                    return es_compatible, "¡El procesador y la placa madre son compatibles!" if es_compatible else "El procesador y la placa madre no son compatibles."
                
                # Comparación entre tarjeta gráfica y placa madre (por el socket)
                elif prod1.tipo_producto.nombre_tipo == 'Graficas' and prod2.tipo_producto.nombre_tipo == 'Placa Madre':
                    es_compatible = comprobar_socket(prod1, prod2)
                    return es_compatible, "¡La tarjeta gráfica y la placa madre son compatibles!" if es_compatible else "La tarjeta gráfica y la placa madre no son compatibles."

                # Comparación entre RAM y placa madre (por la frecuencia)
                elif prod1.tipo_producto.nombre_tipo == 'RAM' and prod2.tipo_producto.nombre_tipo == 'Placa Madre':
                    return prod1.frecuencia_ram <= prod2.frecuencia_ram, "¡La RAM y la placa madre son compatibles!" if prod1.frecuencia_ram <= prod2.frecuencia_ram else "La RAM y la placa madre no son compatibles."
                
                # Comparación entre tarjeta gráfica y procesador (y viceversa)
                elif (prod1.tipo_producto.nombre_tipo == 'Tarjeta Gráfica' and prod2.tipo_producto.nombre_tipo == 'Procesador') or \
                    (prod1.tipo_producto.nombre_tipo == 'Procesador' and prod2.tipo_producto.nombre_tipo == 'Tarjeta Gráfica'):
                    es_compatible = True  # En general, no hay restricción entre estos dos componentes
                    mensaje = "¡La tarjeta gráfica y el procesador son compatibles!"

                    # Verificar si hay cuello de botella
                    frecuencia_boost_procesador = prod1.frecuencia_boost or prod1.frecuencia_base if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.frecuencia_boost or prod2.frecuencia_base
                    nucleos_procesador = prod1.nucleos if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.nucleos
                    hilos_procesador = prod1.hilos if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.hilos
                    memoria_video = prod1.memoria_video if prod1.tipo_producto.nombre_tipo == 'Grafica' else prod2.memoria_video

                    if memoria_video > (nucleos_procesador * 2) and hilos_procesador < 8:
                        mensaje += " Sin embargo, el procesador podría generar un cuello de botella para la tarjeta gráfica."
                    elif frecuencia_boost_procesador > 4.5 and memoria_video < 4:
                        mensaje += " Sin embargo, la tarjeta gráfica podría generar un cuello de botella para el procesador."
                    else:
                        mensaje += " No hay indicios de cuello de botella."
                    return es_compatible, mensaje

                # Si no hay reglas específicas
                else:
                    return False, "No hay reglas definidas para comparar estos productos."

            # Comparar en ambos sentidos
            es_compatible, mensaje = comparar_productos(producto1, producto2)
            if not es_compatible:  # Si no son compatibles en un sentido, probar en el otro
                es_compatible, mensaje = comparar_productos(producto2, producto1)

            return render(request, 'core/plantillas/compatibilidad.html', {
                'producto1': producto1,
                'producto2': producto2,
                'mensaje': mensaje,
                'es_compatible': es_compatible
            })
        else:
            return render(request, 'core/compara.html', {'error': 'Por favor, selecciona dos productos para comparar.'})

    return render(request, 'core/compara.html')


def foro(request):
    # Generar una lista de publicaciones (puedes adaptar esto según tus necesidades)
    publicaciones = range(1, 101)  # Cambia este número según cuántas publicaciones quieras mostrar
    return render(request, 'core/foro.html', {'publicaciones': publicaciones})