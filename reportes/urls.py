from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),
    path('crear/', views.crear_reporte, name='crear_reporte'),
    path('<int:pk>/editar/', views.editar_reporte, name='editar_reporte'),
    path('<int:pk>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),
]