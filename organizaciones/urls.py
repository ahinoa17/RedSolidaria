from django.urls import path
from . import views
from .decorators import superusuario_requerido

urlpatterns = [
    path('', views.lista_organizaciones, name='lista_organizaciones'),
    path('<int:pk>/', views.detalle_organizacion, name='detalle_organizacion'),
    path('crear/', views.crear_organizacion, name='crear_organizacion'),
    path('<int:pk>/editar/', views.editar_organizacion, name='editar_organizacion'),
    path('<int:pk>/eliminar/', views.eliminar_organizacion, name='eliminar_organizacion'),
]