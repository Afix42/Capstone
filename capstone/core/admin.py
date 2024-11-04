from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Producto, TipoProducto,Post,Comentario  

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Personalización de cómo se muestran los usuarios en el admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol',)}),  # Mostrar el campo de rol en el admin
    )

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'contenido', 'post', 'fecha_publicacion')  # Cambia 'fecha_creacion' por 'fecha_publicacion'
    list_filter = ('post', 'autor')  # Filtros en el panel de admin
    search_fields = ('contenido', 'autor__username')  # Búsqueda por contenido o autor

admin.site.register(Rol)  # Registro del modelo Rol
admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(Post)
admin.site.register(Comentario, ComentarioAdmin)