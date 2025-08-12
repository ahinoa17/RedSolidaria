from django.urls import path
from . import views

app_name = 'inscripciones'

urlpatterns = [
    # URLs para usuarios regulares
    path('mis-inscripciones/', views.MisInscripcionesView.as_view(), name='mis_inscripciones'),
    path('inscribirse/<int:oportunidad_id>/', views.inscribirse_oportunidad, name='inscribirse'),
    path('eliminar/<int:pk>/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
    
    # URLs para administradores
    path('gestion/', views.GestionInscripcionesView.as_view(), name='gestion_inscripciones'),
    path('aceptar/<int:pk>/', views.aceptar_inscripcion, name='aceptar_inscripcion'),
    path('rechazar/<int:pk>/', views.rechazar_inscripcion, name='rechazar_inscripcion'),
]