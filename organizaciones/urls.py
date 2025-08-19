# Importa la función path para definir rutas URL
from django.urls import path

# Importa las vistas definidas en el archivo views.py del mismo directorio
from . import views

# Importa el decorador personalizado para restringir acceso a superusuarios
from .decorators import superusuario_requerido

# Lista de patrones de URL para la aplicación de organizaciones
urlpatterns = [
    # URL para listar todas las organizaciones
    # Ejemplo: /organizaciones/
    path('', views.lista_organizaciones, name='lista_organizaciones'),
    
    # URL para ver el detalle de una organización específica
    # <int:pk> captura el ID de la organización como número entero
    # Ejemplo: /organizaciones/1/
    path('<int:pk>/', views.detalle_organizacion, name='detalle_organizacion'),
    
    # URL para crear una nueva organización
    # Ejemplo: /organizaciones/crear/
    path('crear/', views.crear_organizacion, name='crear_organizacion'),
    
    # URL para editar una organización existente
    # <int:pk> captura el ID de la organización a editar
    # Ejemplo: /organizaciones/1/editar/
    path('<int:pk>/editar/', views.editar_organizacion, name='editar_organizacion'),
    
    # URL para eliminar una organización
    # <int:pk> captura el ID de la organización a eliminar
    # Ejemplo: /organizaciones/1/eliminar/
    path('<int:pk>/eliminar/', views.eliminar_organizacion, name='eliminar_organizacion'),
]