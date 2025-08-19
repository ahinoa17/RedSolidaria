# Importa la función 'path' de Django para definir rutas URL
from django.urls import path

# Importa las vistas definidas en el archivo views.py del mismo directorio
from . import views

# Lista que contiene las definiciones de las URLs de la aplicación
urlpatterns = [
    # URL raíz ('') que muestra la lista de oportunidades
    # - '' : ruta raíz
    # - views.lista_oportunidades : vista que maneja esta ruta
    # - name='lista_oportunidades' : nombre único para referenciar esta URL en las plantillas
    path('', views.lista_oportunidades, name='lista_oportunidades'),

    # URL para crear una nueva oportunidad
    # - 'crear/' : ruta que se añade a la URL base
    # - views.crear_oportunidad : vista que maneja la creación
    path('crear/', views.crear_oportunidad, name='crear_oportunidad'),

    # URL para ver el detalle de una oportunidad específica
    # - '<int:pk>/' : captura un parámetro numérico (pk = Primary Key)
    # - int: convierte el parámetro a entero
    # - pk: nombre del parámetro que se pasará a la vista
    path('<int:pk>/', views.detalle_oportunidad, name='detalle_oportunidad'),

    # URL para editar una oportunidad existente
    # - '<int:pk>/editar/' : captura el ID y añade /editar/
    path('<int:pk>/editar/', views.editar_oportunidad, name='editar_oportunidad'),

    # URL para eliminar una oportunidad
    # - '<int:pk>/eliminar/' : captura el ID y añade /eliminar/
    path('<int:pk>/eliminar/', views.eliminar_oportunidad, name='eliminar_oportunidad'),
]