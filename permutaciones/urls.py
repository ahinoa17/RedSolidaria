from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_permutaciones, name='lista_permutaciones'),
    path('crear/', views.crear_permutacion, name='crear_permutacion'),
    path('<int:pk>/editar/', views.editar_permutacion, name='editar_permutacion'),
    path('<int:pk>/eliminar/', views.eliminar_permutacion, name='eliminar_permutacion'),
]