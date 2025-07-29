from django.urls import path
from . import views

urlpatterns = [
    path('mias/', views.mis_inscripciones, name='mis_inscripciones'),
    path('crear/', views.crear_inscripcion, name='crear_inscripcion'),
    path('<int:pk>/editar/', views.editar_inscripcion, name='editar_inscripcion'),
    path('<int:pk>/eliminar/', views.eliminar_inscripcion, name='eliminar_inscripcion'),
]