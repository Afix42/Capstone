from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Producto, TipoProducto,Post,Comentario,Carrito,ItemCarrito

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


class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0
    fields = ('producto', 'cantidad', 'subtotal_display')  # Muestra el subtotal en los inlines
    readonly_fields = ('subtotal_display',)  # Evita edición manual del subtotal

    def subtotal_display(self, obj):
        return f"${obj.subtotal:.2f}" if obj.subtotal else "$0.00"
    subtotal_display.short_description = 'Subtotal'

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado_en', 'total_carrito_display')  # Añade el total del carrito
    inlines = [ItemCarritoInline]

    def total_carrito_display(self, obj):
        return f"${obj.total_carrito:.2f}" if obj.total_carrito else "$0.00"
    total_carrito_display.short_description = 'Total Carrito'

class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'subtotal_display')

    def subtotal_display(self, obj):
        return f"${obj.subtotal:.2f}" if obj.subtotal else "$0.00"
    subtotal_display.short_description = 'Subtotal'

admin.site.register(Rol)  # Registro del modelo Rol
admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(Post)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(ItemCarrito, ItemCarritoAdmin)
