# Importa la función path para definir patrones de URL
from django.urls import path

# Importa las vistas definidas en el mismo directorio
from . import views

# Define el espacio de nombres para las URLs de esta aplicación
# Permite referenciar las URLs como 'inscripciones:nombre_url'
app_name = 'inscripciones'

# Lista de patrones de URL
urlpatterns = [
    # Vista basada en clase que muestra las inscripciones del usuario actual
    # URL: /inscripciones/mis-inscripciones/
    path('mis-inscripciones/', views.MisInscripcionesView.as_view(), name='mis_inscripciones'),
    
    # Vista para inscribirse a una oportunidad específica
    # URL: /inscripciones/inscribirse/1/ (donde 1 es el ID de la oportunidad)
    path('inscribirse/<int:oportunidad_id>/', views.inscribirse_oportunidad, name='inscribirse'),
    
    # Vista para eliminar una inscripción
    # URL: /inscripciones/eliminar/1/ (donde 1 es el ID de la inscripción)
    path('eliminar/<int:pk>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    
    # Vista de administración para gestionar inscripciones (solo administradores)
    # URL: /inscripciones/gestion/
    path('gestion/', views.GestionInscripcionesView.as_view(), name='gestion_inscripciones'),
    
    # Vista para aceptar una inscripción (solo administradores)
    # URL: /inscripciones/aceptar/1/ (donde 1 es el ID de la inscripción)
    path('aceptar/<int:pk>/', views.aceptar_inscripcion, name='aceptar_inscripcion'),
    
    # Vista para rechazar una inscripción (solo administradores)
    # URL: /inscripciones/rechazar/1/ (donde 1 es el ID de la inscripción)
    path('rechazar/<int:pk>/', views.rechazar_inscripcion, name='rechazar_inscripcion'),
]