# Módulo de URLs para la aplicación de permutaciones
# Define las rutas URL para la gestión de solicitudes de permutación

# Importación de la función path para definir patrones de URL
from django.urls import path
# Importación de las vistas definidas en el mismo directorio
from . import views

# Namespace para las URLs de esta aplicación
# Permite referenciar las URLs de forma única en las plantillas
app_name = 'permutaciones'

# Lista de patrones de URL de la aplicación
urlpatterns = [
    # Vista principal que muestra la lista de permutaciones
    # URL: /permutaciones/
    # Usa una vista basada en clase (ListView)
    path('', views.ListaPermutacionesView.as_view(), name='lista'),
    
    # Ruta para crear una nueva solicitud de permutación
    # URL: /permutaciones/solicitar/<id_oportunidad>/
    # <int:oportunidad_id> - ID numérico de la oportunidad objetivo
    path('solicitar/<int:oportunidad_id>/', views.crear_solicitud, name='crear'),
    
    # Ruta para ver los detalles de una solicitud específica
    # URL: /permutaciones/solicitud/<id_solicitud>/
    # <int:pk> - ID numérico de la solicitud (primary key)
    path('solicitud/<int:pk>/', views.DetalleSolicitudView.as_view(), name='detalle_solicitud'),
    
    # Ruta para aceptar una solicitud de permutación
    # URL: /permutaciones/solicitud/<id_solicitud>/aceptar/
    path('solicitud/<int:pk>/aceptar/', views.aceptar_solicitud, name='aceptar'),
    
    # Ruta para rechazar una solicitud de permutación
    # URL: /permutaciones/solicitud/<id_solicitud>/rechazar/
    path('solicitud/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar'),
    
    # Ruta para cancelar una solicitud de permutación
    # URL: /permutaciones/solicitud/<id_solicitud>/cancelar/
    path('solicitud/<int:pk>/cancelar/', views.cancelar_solicitud, name='cancelar'),
]