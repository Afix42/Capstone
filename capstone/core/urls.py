# urls.py
from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # Esta es la ruta a la que necesitas apuntar
    path('foro/', views.foro, name='foro'),
    path('tienda/', views.tienda, name='tienda'),
    path('usuario/', views.vista_usuario, name='usuario'),
    path('admin/', views.vista_admin, name='admin'),
    path('registro/', views.registro_view, name='registro'),
    path('inicio_sesion/', views.funcion_login, name='login'),  # Esta es la función que maneja el login
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),   
    path('compara/', views.compara, name='compara'),
    path('comprobar_compatibilidad/', views.comprobar_compatibilidad, name='comprobar_compatibilidad'),
    path('cerrar_sesion/', views.funcion_logout, name='cerrar_sesion'),
    path('registrar/',views.registro_view, name='registrarse'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar-contraseña/', views.change_password, name='change_password'),
    path('tienda/formEditProducto/<int:producto_id>/', views.form_edit_prod, name='formEditProd'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('crear_post',views.crear_post, name='crear_post' ),
    path('agregar_producto/', views.formAgregarProd, name='agregar_producto'),
    path('tienda/eliminar_producto/<int:producto_id>/',views.eliminar_producto, name='eliminar_producto'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    

    path('ruta-ajax-compatibilidad/', views.obtener_compatibles, name='ruta-ajax-compatibilidad'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
