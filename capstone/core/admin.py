from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Producto, TipoProducto,Post

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Personalización de cómo se muestran los usuarios en el admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol',)}),  # Mostrar el campo de rol en el admin
    )

admin.site.register(Rol)  # Registro del modelo Rol
admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(Post)