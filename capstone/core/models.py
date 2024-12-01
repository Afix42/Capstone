from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from decimal import Decimal

# Create your models here.


class Rol(models.Model):
    nombreRol = models.CharField(max_length=25, verbose_name='El nombre del rol de usuario')

    def __str__(self):
        return self.nombreRol
    
    
class Usuario(AbstractUser):
    # Los grupos y permisos ya están gestionados por Django en el modelo de usuario
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='grupos_usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permisos')
    
    # Puedes agregar campos adicionales si necesitas
    # otros campos personalizados, como el relacionado con tu modelo de rol:
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Rol de Usuario')
    foto_perfil = models.ImageField(upload_to='foto_perfil/', null=True, blank=True, default='foto_perfil/default.jpg')

    # Campo para almacenar el código de recuperación de contraseña
    codigo_recuperacion = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def generar_codigo_recuperacion(self):
        self.codigo_recuperacion = get_random_string(length=6, allowed_chars='0123456789')
        self.save()
class TipoProducto(models.Model):
    nombre_tipo = models.CharField(max_length=25, verbose_name='Nombre del tipo de producto')
    
    def __str__(self):
        return self.nombre_tipo

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=255, verbose_name='Nombre del producto')
    descripcion_producto = models.TextField(verbose_name='Descripción del producto')
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio del producto', default=0)
    stock_producto = models.IntegerField(verbose_name='Stock del producto', default=0)
    imagen_uno = models.ImageField(upload_to="productos/", verbose_name='Primera imagen')
    imagen_dos = models.ImageField(upload_to="productos/", verbose_name='Segunda imagen', null=True, blank=True)
    imagen_tres = models.ImageField(upload_to="productos/", verbose_name='Tercera imagen', null=True, blank=True)
    imagen_cuatro = models.ImageField(upload_to="productos/", verbose_name='Cuarta imagen', null=True, blank=True)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, verbose_name='Tipo de producto', null=True)
    activo = models.BooleanField(default=True)  # Campo para borrado suave
    # Campos generales para productos tecnológicos
    marca = models.CharField(max_length=50, verbose_name='Marca del producto', null=True, blank=True)
    modelo = models.CharField(max_length=100, verbose_name='Modelo del producto', null=True, blank=True)
    socket = models.CharField(max_length=100, verbose_name='Sockets que contiene el componente', null=True, blank=True)

    # Campos específicos para productos como tarjetas gráficas
    memoria_video = models.IntegerField(verbose_name='Memoria VRAM (GB)', null=True, blank=True, default=0)
    tipo_memoria = models.CharField(max_length=10, verbose_name='Tipo de memoria', null=True, blank=True)  # Para RAM o tarjeta gráfica

    # Campos específicos para otros componentes como almacenamiento o RAM
    capacidad_almacenamiento = models.IntegerField(verbose_name='Capacidad de almacenamiento (GB)', null=True, blank=True)  # Para discos duros
    frecuencia_ram = models.IntegerField(verbose_name='Frecuencia RAM (MHz)', null=True, blank=True)  # Para memorias RAM

    # Campos para SSDS o Discos Duros
    velocidad_lectura = models.IntegerField(verbose_name='Velocidad de lectura (MB/s)', null=True, blank=True)
    velocidad_escritura = models.IntegerField(verbose_name='Velocidad de escritura (MB/s)', null=True, blank=True)

    # Campos para procesadores
    frecuencia_base = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Frecuencia base (GHz)', null=True, blank=True, default=0)
    frecuencia_boost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Frecuencia boost (GHz)', null=True, blank=True, default=0)
    nucleos = models.IntegerField(verbose_name='Número de núcleos', null=True, blank=True, default=0)
    hilos = models.IntegerField(verbose_name='Número de hilos', null=True, blank=True, default=0)
    
    def __str__(self):
        return self.nombre_producto
    
class Post(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    # Aquí agregamos el campo ManyToManyField para los likes y le damos un nombre único con `related_name`
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return self.titulo
    
    @property
    def total_likes(self):
        return self.likes.count()  # Cuenta los likes relacionados con este post
    

class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes_related", on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="likes_given", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'usuario')  # Evita duplicados

    def __str__(self):
        return f"{self.usuario} le dio like a {self.post.titulo}"

class Comentario(models.Model):
    post = models.ForeignKey(Post, related_name="comentarios", on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor} en {self.post}"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carritos')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    @property
    def total_carrito(self):
        return sum(item.subtotal for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return Decimal(self.producto.precio_producto) * Decimal(self.cantidad)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto}"
    

