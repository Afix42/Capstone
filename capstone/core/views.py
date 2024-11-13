from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_login
from .models import Usuario, Rol, Producto, TipoProducto, Post, Comentario, Like
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import PostForm, ComentarioForm
import logging
import requests
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



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

def tienda(request):
    tipo_graficas = TipoProducto.objects.get(nombre_tipo='Graficas')  # Asegúrate de que 'Graficas' existe
    tipo_procesador = TipoProducto.objects.get(nombre_tipo='Procesador')
    tipo_placamadre = TipoProducto.objects.get(nombre_tipo='Placa Madre')
    if request.user.is_staff:
        productos_graficas = Producto.objects.filter(tipo_producto=tipo_graficas)  # Filtrar productos
        productos_procesador = Producto.objects.filter(tipo_producto=tipo_procesador)
        productos_placamadre = Producto.objects.filter(tipo_producto=tipo_placamadre)
    else:
        productos_graficas = Producto.objects.filter(tipo_producto=tipo_graficas, activo=True)  # Filtrar productos
        productos_procesador = Producto.objects.filter(tipo_producto=tipo_procesador, activo=True)
        productos_placamadre = Producto.objects.filter(tipo_producto=tipo_placamadre, activo=True)
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




# Función para verificar si el correo existe a través de un servicio externo
def verificar_correo_existe(email):
    api_key = '087d0aa017eb98b860b3b335816ef830142e2c04'
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    # Comprueba el estado de la respuesta de la API (esto depende del servicio de verificación que uses)
    if response.status_code == 200 and data['data']['status'] == 'valid':
        return True
    return False

from django.core.mail import send_mail
from django.conf import settings

def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['confirm_password']

        # Validación de formato de correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'El formato del correo electrónico es inválido.')
            return render(request, 'core/form_registro.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'core/form_registro.html')

        # Verificación de existencia del correo mediante la API
        if not verificar_correo_existe(email):
            messages.error(request, 'La dirección de correo electrónico no es válida o no existe.')
            return render(request, 'core/form_registro.html')

        if password == repeat_password:
            try:
                user = Usuario.objects.create_user(username=username, email=email, password=password)
                
                # Asignar rol predeterminado
                rol_predeterminado = Rol.objects.get(nombreRol='Usuario')
                user.rol = rol_predeterminado
                user.save()
                
                # Enviar correo de confirmación
                asunto = '¡Registro exitoso en nuestra plataforma!'
                mensaje = f'Hola {username},\n\nGracias por registrarte en nuestra plataforma. Tu cuenta ha sido creada exitosamente.'
                remitente = settings.DEFAULT_FROM_EMAIL
                destinatario = [email]

                send_mail(asunto, mensaje, remitente, destinatario)

                messages.success(request, 'Usuario registrado exitosamente. Revisa tu correo para más detalles.')
                return redirect('login')
            
            except IntegrityError as e:
                messages.error(request, 'Error al registrar el usuario.')
            except Exception as e:
                messages.error(request, f'Error inesperado: {str(e)}')
        else:
            messages.error(request, 'Las contraseñas no coinciden')

    return render(request, 'core/form_registro.html')






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





# archivo views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def obtener_compatibles(request):    
    id_producto1 = request.GET.get('producto1')
    tipo_producto2_id = request.GET.get('tipo_producto2')  # Nuevo parámetro de tipo
    mensaje = "Productos compatibles encontrados."
    compatibles_data = []
    tipos_compatibles_data = []

    if id_producto1:
        producto1 = get_object_or_404(Producto, id=id_producto1)

        # Determina los tipos compatibles basados en el tipo de producto1
        tipos_compatibles = []
        if producto1.tipo_producto.nombre_tipo == 'Procesador':
            tipos_compatibles.extend(['Graficas', 'Placa Madre'])

        elif producto1.tipo_producto.nombre_tipo == 'Graficas':
            tipos_compatibles.extend(['Procesador', 'Placa Madre'])
            
        elif producto1.tipo_producto.nombre_tipo == 'Placa Madre':
            tipos_compatibles.extend(['Graficas', 'Procesador'])

        # Filtrar productos compatibles según el tipo seleccionado en el frontend (si existe)
        compatibles = Producto.objects.filter(tipo_producto__nombre_tipo__in=tipos_compatibles)
        if tipo_producto2_id:
            compatibles = compatibles.filter(tipo_producto_id=tipo_producto2_id)

        # Preparar los datos de productos compatibles
        compatibles_data = [
            {
                'id': p.id,
                'nombre': p.nombre_producto,
                'imagen_uno': p.imagen_uno.url,
                'precio_producto': p.precio_producto
            }
            for p in compatibles
        ]

        # Preparar los tipos compatibles para la respuesta
        tipos_compatibles_data = [
            {
                'id': tipo.id,
                'nombre_tipo': tipo.nombre_tipo
            }
            for tipo in TipoProducto.objects.filter(nombre_tipo__in=tipos_compatibles)
        ]

    return JsonResponse({'compatibles': compatibles_data, 'tiposCompatibles': tipos_compatibles_data, 'mensaje': mensaje})




def comprobar_compatibilidad(request):
    compatibles = []  # Inicializar la lista de compatibles
    mensaje = ""

    if request.method == 'GET':
        id_producto1 = request.GET.get('producto1')
        id_producto2 = request.GET.get('producto2')

        # Si se ha seleccionado el primer producto
        if id_producto1:
            producto1 = get_object_or_404(Producto, id=id_producto1)

            # Filtrar productos compatibles según el tipo del primer producto
            tipos_compatibles = ['Placa Madre']  # Ajusta según tu lógica de compatibilidad
            if producto1.tipo_producto.nombre_tipo == 'Procesador':
                tipos_compatibles.append('Tarjeta Gráfica')
            elif producto1.tipo_producto.nombre_tipo == 'Tarjeta Gráfica':
                tipos_compatibles.append('Procesador')

            compatibles = Producto.objects.filter(tipo_producto__nombre_tipo__in=tipos_compatibles)

            # Si también se ha seleccionado el segundo producto, comprobar compatibilidad
            if id_producto2:
                producto2 = get_object_or_404(Producto, id=id_producto2)
                es_compatible, mensaje = comparar_productos(producto1, producto2)

                return render(request, 'core/plantillas/compatibilidad.html', {
                    'producto1': producto1,
                    'producto2': producto2,
                    'mensaje': mensaje,
                    'es_compatible': es_compatible
                })

            # Si solo hay un producto seleccionado, renderizar la plantilla de comparación
            return render(request, 'core/compara.html', {
                'tipos': TipoProducto.objects.all(),
                'productos': Producto.objects.all(),
                'compatibles': compatibles,
                'mensaje': mensaje,
            })

    # En caso de que no se seleccione ningún producto, mostrar la plantilla de comparación sin resultados
    return render(request, 'core/compara.html', {
        'tipos': TipoProducto.objects.all(),
        'productos': Producto.objects.all(),
        'compatibles': compatibles,
        'mensaje': mensaje,
    })



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
                if (prod1.tipo_producto.nombre_tipo == 'Placa Madre' and prod2.tipo_producto.nombre_tipo == 'Procesador') or \
                    (prod1.tipo_producto.nombre_tipo == 'Procesador' and prod2.tipo_producto.nombre_tipo == 'Placa Madre'):
                    es_compatible = comprobar_socket(prod1, prod2)
                    return es_compatible, "¡El procesador y la placa madre son compatibles!" if es_compatible else "El procesador y la placa madre no son compatibles."
                
                # Comparación entre tarjeta gráfica y placa madre (por el socket)
                elif (prod1.tipo_producto.nombre_tipo == 'Placa Madre' and prod2.tipo_producto.nombre_tipo == 'Graficas') or \
                    (prod1.tipo_producto.nombre_tipo == 'Graficas' and prod2.tipo_producto.nombre_tipo == 'Placa Madre'):
                    es_compatible = comprobar_socket(prod1, prod2)
                    return es_compatible, "¡La tarjeta gráfica y la placa madre son compatibles!" if es_compatible else "La tarjeta gráfica y la placa madre no son compatibles."

                # Comparación entre RAM y placa madre (por la frecuencia)
                elif prod1.tipo_producto.nombre_tipo == 'RAM' and prod2.tipo_producto.nombre_tipo == 'Placa Madre':
                    return prod1.frecuencia_ram <= prod2.frecuencia_ram, "¡La RAM y la placa madre son compatibles!" if prod1.frecuencia_ram <= prod2.frecuencia_ram else "La RAM y la placa madre no son compatibles."
                
                # Comparación entre tarjeta gráfica y procesador (y viceversa)
                elif (prod1.tipo_producto.nombre_tipo == 'Graficas' and prod2.tipo_producto.nombre_tipo == 'Procesador') or \
        (prod1.tipo_producto.nombre_tipo == 'Procesador' and prod2.tipo_producto.nombre_tipo == 'Graficas'):

                    es_compatible = True
                    mensaje = "¡La tarjeta gráfica y el procesador son compatibles!"

                    # Obtener datos de frecuencia, núcleos, hilos y memoria de video
                    frecuencia_boost_procesador = (
                        prod1.frecuencia_boost if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.frecuencia_boost
                    ) or (
                        prod1.frecuencia_base if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.frecuencia_base
                    )
                    nucleos_procesador = prod1.nucleos if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.nucleos
                    hilos_procesador = prod1.hilos if prod1.tipo_producto.nombre_tipo == 'Procesador' else prod2.hilos
                    memoria_video = prod1.memoria_video if prod1.tipo_producto.nombre_tipo == 'Graficas' else prod2.memoria_video

                    # Verificar si tenemos toda la información necesaria
                    if frecuencia_boost_procesador is not None and nucleos_procesador is not None and \
                            hilos_procesador is not None and memoria_video is not None:

                        # Condiciones mejoradas para detectar el cuello de botella
                        if memoria_video > (nucleos_procesador * 2) and hilos_procesador <= 8:
                            mensaje += " Sin embargo, el procesador podría generar un cuello de botella para la tarjeta gráfica debido a un número limitado de hilos."
                        elif frecuencia_boost_procesador > 4.0 and memoria_video < 8:
                            mensaje += " Sin embargo, la tarjeta gráfica podría generar un cuello de botella para el procesador debido a una frecuencia elevada con poca memoria de video."
                        elif nucleos_procesador < 4 and frecuencia_boost_procesador < 3.0:
                            mensaje += " El procesador tiene pocos núcleos y frecuencia baja, lo que podría limitar el rendimiento de la tarjeta gráfica."
                        elif frecuencia_boost_procesador > 5.0 and memoria_video < 4:
                            mensaje += " El procesador tiene una frecuencia muy alta, pero la tarjeta gráfica podría ser el cuello de botella debido a su baja memoria."
                        elif nucleos_procesador < 6 and memoria_video > 6:
                            mensaje += " El procesador con pocos núcleos podría limitar el rendimiento de la tarjeta gráfica."
                        elif nucleos_procesador < 4 and frecuencia_boost_procesador < 3.5:
                            mensaje += " El procesador podría ser el cuello de botella, ya que tiene pocos núcleos y frecuencia baja para aprovechar la tarjeta gráfica."
                        elif memoria_video > 8 and frecuencia_boost_procesador <= 3.5:
                            mensaje += " La tarjeta gráfica tiene más memoria de la que el procesador puede manejar eficientemente, generando un cuello de botella."
                        else:
                            mensaje += " No hay indicios claros de cuello de botella."
                    else:
                        mensaje += " Sin embargo, no hay suficiente información para evaluar el cuello de botella."

                    return es_compatible, mensaje


                # Si no hay reglas específicas

                else:
                    return False, "No hay reglas definidas para comparar estos productos."


# Vista para la lista de posts, ahora renombrada a 'foro'
def foro(request):
    # Ordenar por el campo correcto que es 'fecha_publicacion'
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'core/foro.html', {'posts': posts})

logger = logging.getLogger(__name__)

# Vista para el detalle de un post, ahora renombrada a 'post'

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = post.comentarios.all()  # Obtener comentarios relacionados con el post

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post  # Asignar el post al comentario
            comentario.autor = request.user  # Asignar el autor al comentario
            comentario.save()
            return redirect('post', post_id=post.id)  # Redirigir a la misma página
    else:
        form = ComentarioForm()

    # Pasamos el total de likes en `like_count` al contexto
    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
        'like_count': post.total_likes,  # Pasamos el total de likes usando la propiedad `total_likes`
    }
    return render(request, 'post.html', context)

# Vista para crear un post
from django.shortcuts import render, redirect
from .models import Post  # Asegúrate de que tu modelo Post esté importado
from .forms import PostForm  # Asegúrate de que tu formulario de Post esté importado

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.autor = request.user  
            post.save()  
            return redirect('foro')
    else:
        form = PostForm()
    return render(request, 'core/form_crear_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Obtener el post por su ID
    comentarios = post.comentarios.all()  # Obtener todos los comentarios relacionados con el post

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post  # Asignar el post al comentario
            comentario.autor = request.user  # Asignar el autor del comentario
            comentario.save()
            return redirect('post_detail', post_id=post.id)  # Redirigir a la misma página después de guardar el comentario
    else:
        form = ComentarioForm()  # Crear un nuevo formulario vacío si no es POST

    context = {
        'post': post,  # Pasar el post al contexto
        'comentarios': comentarios,  # Pasar los comentarios al contexto
        'form': form,  # Pasar el formulario al contexto
    }
    return render(request, 'core/post.html', context)  # Renderizar la plantilla

@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    user = request.user

    # Lógica para actualizar el conteo de likes
    if user.is_authenticated:
        if user in post.likes.all():
            post.likes.remove(user)  # Quita el "like"
        else:
            post.likes.add(user)  # Agrega el "like"
        
        # Retorna el nuevo conteo de likes
        return JsonResponse({"like_count": post.likes.count()})
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)


def form_edit_prod(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    tipo_producto = TipoProducto.objects.all()
    
    if request.method == 'POST':
        # Usa los nombres de los campos en el formulario HTML
        producto.nombre_producto = request.POST.get('nomProd')
        producto.descripcion_producto = request.POST.get('descripcionProducto')
        producto.precio_producto = request.POST.get('precioProducto')
        producto.stock_producto = request.POST.get('stockProducto')
        # Manejar el campo de estado "activo"
        producto.activo = 'activo' in request.POST  # Quedará activo si la checkbox está marcada
        # Relación con TipoProducto (asumiendo que tipo_producto es una relación FK en Producto)
        tipo_producto_nombre = request.POST.get('tipo_producto')
        producto.tipo_producto = TipoProducto.objects.get(nombre_tipo=tipo_producto_nombre)

        # Actualizar las imágenes solo si se proporcionan nuevos archivos
        if 'imagenUno' in request.FILES:
            producto.imagen_uno = request.FILES['imagenUno']
        if 'imagenDos' in request.FILES:
            producto.imagen_dos = request.FILES['imagenDos']
        if 'imagenTres' in request.FILES:
            producto.imagen_tres = request.FILES['imagenTres']
        if 'imagenCuatro' in request.FILES:
            producto.imagen_cuatro = request.FILES['imagenCuatro']

        messages.success(request, 'Producto modificado correctamente')
        producto.save()

    return render(request, 'core/form_editar_productos.html', {'producto': producto, 'tipo_producto': tipo_producto})

def formAgregarProd(request):
    tipo_producto = TipoProducto.objects.all()
    if request.method == "POST":
        pro = Producto()
        pro.nombre_producto = request.POST.get('nomProd')
        pro.descripcion_producto = request.POST.get('descripcionProducto')
        pro.precio_producto = request.POST.get('precioProducto')
        pro.stock_producto = request.POST.get('stockProducto')

        # Buscar el tipo de producto en la base de datos
        tipo_producto_nombre = request.POST.get('tipo_producto')
        ti_producto = TipoProducto.objects.filter(nombre_tipo=tipo_producto_nombre).first()

        # Verificar si el tipo de producto existe
        if ti_producto:
            pro.tipo_producto = ti_producto
        else:
            messages.error(request, 'Tipo de producto no válido')
            return redirect('agregar_producto')

        # Guardar imágenes
        pro.imagen_uno = request.FILES.get('imagenUno')
        pro.imagen_dos = request.FILES.get('imagenDos')
        pro.imagen_tres = request.FILES.get('imagenTres')
        pro.imagen_cuatro = request.FILES.get('imagenCuatro')

        # Guardar el producto
        try:
            pro.save()
            messages.success(request, 'Producto agregado correctamente')
            return redirect('agregar_producto')
        except Exception as e:
            messages.error(request, f'No se pudo agregar el producto: {str(e)}')

    return render(request, 'core/form_agregar_productos.html', {'tipo_producto': tipo_producto})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = False  # Cambiar el estado a inactivo
    producto.save()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('tienda')  # Redirigir a la lista de productos