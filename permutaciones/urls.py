# permutaciones/urls.py
from django.urls import path
from . import views

app_name = 'permutaciones'

urlpatterns = [
    # Lista de permutaciones (usando la vista basada en clases)
    path('', views.ListaPermutacionesView.as_view(), name='lista'),
    
    # Crear nueva solicitud de permutación
    path('solicitar/<int:oportunidad_id>/', views.crear_solicitud, name='crear'),
    
    # Gestionar solicitudes existentes
    path('solicitud/<int:pk>/', views.DetalleSolicitudView.as_view(), name='detalle_solicitud'),
    path('solicitud/<int:pk>/aceptar/', views.aceptar_solicitud, name='aceptar'),
    path('solicitud/<int:pk>/rechazar/', views.rechazar_solicitud, name='rechazar'),
    path('solicitud/<int:pk>/cancelar/', views.cancelar_solicitud, name='cancelar'),
]