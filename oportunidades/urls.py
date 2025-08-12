from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_oportunidades, name='lista_oportunidades'),
    path('crear/', views.crear_oportunidad, name='crear_oportunidad'),
    path('<int:pk>/', views.detalle_oportunidad, name='detalle_oportunidad'),
    path('<int:pk>/editar/', views.editar_oportunidad, name='editar_oportunidad'),
    path('<int:pk>/eliminar/', views.eliminar_oportunidad, name='eliminar_oportunidad'),
]