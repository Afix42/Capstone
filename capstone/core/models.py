from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# Create your models here.


class Rol(models.Model):
    nombreRol = models.CharField(max_length=25, verbose_name='El nombre del rol de usuario')

    def __str__(self):
        return self.nombreRol
    
    
class Usuario(AbstractUser):
    # Los grupos y permisos ya están gestionados por Django en el modelo de usuario
    groups = models.ManyToManyField(Group, related_name='grupos_usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permisos')
    
    # Puedes agregar campos adicionales si necesitas
    # otros campos personalizados, como el relacionado con tu modelo de rol:
    rol = models.ForeignKey('Rol', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Rol de Usuario')

    def __str__(self):
        return self.username